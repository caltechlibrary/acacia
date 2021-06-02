'''
server.py: Acacia server definition.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import bottle
from   bottle import Bottle, HTTPResponse, static_file, template
from   bottle import request, response, redirect, route, get, post, error
from   commonpy.network_utils import net
from   datetime import datetime as dt
from   datetime import timedelta as delta
from   dateutil import tz
from   decouple import config
from   enum import Enum, auto
from   expiringdict import ExpiringDict
from   fdsend import send_file
import functools
from   humanize import naturaldelta
import inspect
from   io import BytesIO
import json
import os
from   os.path import realpath, dirname, join, exists, isabs
from   peewee import *
import random
from   sidetrack import log, logr
from   str2bool import str2bool
import string
import sys
from   textwrap import shorten

from . import __version__

# Acacia Code
from .persons import Person, person_from_environ
from .roles import role_to_redirect, has_role, staff_user
from .messages import Message, EMailProcessor
from .doi import Workflow, Doi, DOIProcessor
from .eprints import EPrintsSSH


# General configuration and initialization.
# .............................................................................

# Begin by creating a Bottle object on which we will define routes and other
# behaviors in the rest of this file.
acacia = Bottle()

# Construct the path to the server root, which we use to construct other paths.
_SERVER_ROOT = realpath(join(dirname(__file__), os.pardir))

# Tell Bottle where to find templates.  This is necessary for both the Bottle
# template() command to work and also to get %include to work inside our .tpl
# template files.  Rather surprisingly, the only way to tell Bottle where to
# find the templates is to set this Bottle package-level variable.
bottle.TEMPLATE_PATH.append(join(_SERVER_ROOT, 'acacia', 'templates'))

# Where we send users to give feedback.
_FEEDBACK_URL = config('FEEDBACK_URL', default = '/')

# Where we send users for help.
_HELP_URL = config('HELP_URL', default = 'https://caltechlibrary.github.io/acacia')


# General-purpose utilities used repeatedly.
# .............................................................................

def page(name, **kargs):
    '''Create a page using template "name" with some standard variables set.'''
#FIXME: we're alling person_from_environ multiple times per request,
# maybe this should happend once in a bottle plugin and all requests
# should have a person object or person as None.
    person = person_from_environ(request.environ)
    logged_in = (person != None and person.uname != '')
    if kargs.get('browser_no_cache', False):
        response.add_header('Expires', '0')
        response.add_header('Pragma', 'no-cache')
        response.add_header('Cache-Control',
                            'no-store, max-age=0, no-cache, must-revalidate')
    return template(name, base_url = acacia.base_url, version = __version__,
                    logged_in = logged_in, staff_user = staff_user(person),
                    help_url = _HELP_URL, **kargs)


def debug_mode():
    '''Return True if we're running Bottle's default server in debug mode.'''
    return getattr(acacia, 'debug_mode', False)



# Bespoke, locally-sourced, artisanal Bottle plugins.
# .............................................................................
# Bottle's "plugins" are basically like Python decorators.  They're most
# useful when you have a decorator that you would otherwise want to put on
# every route (and which would therefore clutter your source code with a lot
# of repetitive calls to @foo decorators).  Bottle calls the plugins in the
# Bottle @get/@post/@route functions, and like Python decorators, a given
# plugin is only applied once to a given route (because what a plugin does is
# wrap a function with another function).  Tip: if you also have decorators
# that you want be added to a route, put the decorators highest, above the
# call to @acacia.get/@acacia.post.

class BottlePluginBase(object):
    '''Base class for Bottle plugins for Acacia.'''
    # This sets the Bottle API version. It defaults to v.1. See
    # https://bottlepy.org/docs/dev/plugindev.html#plugin-api-changes
    api = 2


class RouteTracer(BottlePluginBase):
    '''Write a log entry for this route invocation.'''

    def apply(self, callback, route):
        def route_tracer(*args, **kwargs):
            person = person_from_environ(request.environ)
            log(f'{route.method} {route.rule} invoked'
                + (f' by {person.uname}' if person else ''))
            return callback(*args, **kwargs)

        return route_tracer


# Hook in the plugins above into all routes.
acacia.install(RouteTracer())

# The remaining plugins below are applied selectively to specific routes only.


class VerifyStaffUser(BottlePluginBase):
    '''Redirect to an error page if the user lacks sufficient priviledges.'''
    def apply(self, callback, route):
        def staff_person_plugin_wrapper(*args, **kwargs):
            person = person_from_environ(request.environ)
            if person is None:
                log(f'person is None')
                return page('error', person, summary = 'authentication failure',
                            message = f'Unrecognized user identity.')
            if not staff_user(person):
                log(f'{request.path} invoked by non-staff user {person.uname}')
                redirect(f'{acacia.base_url}/notallowed')
                return
            return callback(*args, **kwargs)
        return staff_person_plugin_wrapper


# Administrative interface endpoints.
# .............................................................................

# A note about authentication: the entire Acacia application is assumed to be
# behind a server that implements authentication, for example using SSO.
# This means we never need to log a person in: they will be authenticated by
# SSO before they can get to Acacia pages.  However, once in Acacia, we do need
# to provide a way for them to un-authenticate themselves.  This is the
# reason for the asymmetry between /logout and (lack of) login.

@acacia.post('/logout')
def logout():
    '''Handle the logout action from the navbar menu on every page.'''
    # If we are not in debug mode, then whether the user is authenticated or
    # not is determined by the presence of REMOTE_USER.
    if request.environ.get('REMOTE_USER', None) and not debug_mode():
        redirect(f'/Shibboleth.sso/Logout')
    else:
        redirect('/')


@acacia.get('/', apply = VerifyStaffUser())
@acacia.get('/manage', apply = VerifyStaffUser())
def manage_items():
    '''Manage the DOI retrieval requests.'''
    return page('manage') 


@acacia.get('/add', apply = VerifyStaffUser())
def add():
    '''Display a page to add a new DOI retrieval request.'''
    return page('edit', action = 'add', doi = None)


@acacia.get('/edit/<doi>', apply = VerifyStaffUser())
def edit(doi):
    '''Display a page to edit a DOI retreival request.'''
#FIXME: retrieve the DOI object include the DOI and object_url
    doi = {"doi": "123340/1223345.03333", "object_url": "https://example.edu/my.pdf" }
    return page('edit', action = 'edit', **doi)


@acacia.post('/update/add', apply = VerifyStaffUser())
@acacia.post('/update/edit', apply = VerifyStaffUser())
def update_item():
    '''Handle http POST requests for adding/editing DOI retrieval requests.'''
    if 'cancel' in request.POST:
        log(f'user clicked Cancel button')
        redirect(f'{acacia.base_url}/manage')
        return

    # The HTML form validates the data types, but the POST might come from
    # elsewhere, so we always need to sanity-check the values.

# FIXME: Need to implement adding/updating a DOI POST
    doi_str = request.POST.doi.strip()
    object_url = request.POST.pdf.string()
    redirect(f'{acacia.base_url}/manage')


@acacia.post('/remove', apply = VerifyStaffUser())
def remove_item():
    '''Handle HTTP POST request to remove a DOI retrieval request.'''
# FIXME: Need to implement remove DOI POST
    doi_str = request.POST.doi.strip()
    redirect(f'{acacia.base_url}/manage')



# User endpoints.
# .............................................................................

@acacia.get('/about')
def general_page(name = '/'):
    '''Display the About page.'''
    return page('about')



# Error pages.
# .............................................................................
# Note: the Bottle session plugin does not seem to supply session arg to @error.

@acacia.get('/notallowed')
@acacia.post('/notallowed')
def not_allowed():
    return page('error', summary = 'access error',
                message = ('The requested page does not exist or you do not '
                           'not have permission to access the requested item.'))

@acacia.error(404)
def error404(error):
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('404', code = error.status_code, message = error.body)


@acacia.error(405)
def error405(error):
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('error', summary = 'method not allowed',
                message = ('The requested method does not exist or you do not '
                           'not have permission to perform the action.'))


# Miscellaneous static pages.
# .............................................................................

@acacia.get('/favicon.ico')
def favicon():
    '''Return the favicon.'''
    return static_file('favicon.ico', root = 'acacia/static')


@acacia.get('/static/<filename:re:[-a-zA-Z0-9]+.(ico|png|jpg|svg)>')
def include_file(filename):
    '''Return a static file'''
    log(f'returning included file {filename}')
    return static_file(filename, root = 'acacia/static')

@acacia.get('/static/assets/<filename:re:[-a-zA-Z0-9]+.(gif|png|jpg|svg)>')
def included_assets_file(filename):
    '''Return a static file used with %include in a template.'''
    log(f'returning included assets file {filename}')
    return static_file(filename, root = 'acacia/static/assets')

@acacia.get('/static/css/<filename:re:[-a-zA-Z0-9]+.(css)>')
def included_css_file(filename):
    '''Return a static file used with %include in a template.'''
    log(f'returning included CSS file {filename}')
    return static_file(filename, root = 'acacia/static/css')

