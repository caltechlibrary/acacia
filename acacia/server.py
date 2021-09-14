'''
server.py: Acacia server definition.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''
import os
import logging
from time import strftime

from decouple import config

import bottle
from   bottle import Bottle, HTTPResponse, static_file, template
from   bottle import request, response, redirect, route, get, post, error

from . import __version__

# Acacia Code
from .persons import Person, person_from_environ
from .roles import role_to_redirect, has_role, staff_user
from .messages import Message, EMailProcessor
from .doi import Workflow, Doi, DOIProcessor, validate_doi
from .eprints import EPrintsSSH

if __debug__:
    from sidetrack import set_debug, log


# General configuration and initialization.
# .............................................................................

# Begin by creating a Bottle object on which we will define routes and other
# behaviors in the rest of this file.
acacia = Bottle()

# Construct the path to the server root, which we use to construct other paths.
_SERVER_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))

# Tell Bottle where to find templates.  This is necessary for both the Bottle
# template() command to work and also to get %include to work inside our .tpl
# template files.  Rather surprisingly, the only way to tell Bottle where to
# find the templates is to set this Bottle package-level variable.
bottle.TEMPLATE_PATH.append(os.path.join(_SERVER_ROOT, 'templates'))

_HELP_URL = '/help/'

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

def xml_page(data, **kargs):
    content_type = 'application/xml'
    content_type = kargs.get('content_type', 'application/xml')
    response.add_header('Content-Type', content_type)
    return data

def debug_mode():
    '''Return True if we're running Bottle's default server in debug mode.'''
    return getattr(acacia, 'debug_mode', False)


#
# URL end points
# .....................................................................
#

# A note about authentication: the entire Acacia application is assumed
# to be behind a server that implements authentication, for example
# using SSO. This means we never need to log a person in: they will be
# authenticated by SSO before they can get to Acacia pages.  However,
# once in Acacia, we do need to provide a way for them to un-authenticate
# themselves.  This is the reason for the asymmetry between /logout
# and (lack of) login.

@acacia.post('/logout')
def logout():
    '''Handle the logout action from the navbar menu on every page.'''
    # If we are not in debug mode, then whether the user is authenticated or
    # not is determined by the presence of REMOTE_USER.
    if request.environ.get('REMOTE_USER', None) and not debug_mode():
        redirect(f'/Shibboleth.sso/Logout')
    else:
        redirect('/')

#
# NOTE: End points for Acacia need to provide for four page activities
# 
# 1. Dashboard provides a page that lists activities (this is a static page)
# 2. Dois lists pending DOI to be exported to EPrints
#    - Per row cells
#      - DOI linked to the https/doi.org URL
#      - link to DOI record at CrossRef or DataCite
#      - Link to view the PDF to download, a select box to include PDF
#        in bundle of specific DOI to be bundled for export
#      - Checkbox to include in a export bundle of EPrints XML
#      - Checkbox to include PDF a export bundle
#      - Button to put DOI in trash
# 3. Bundles lists export bundles ready to download
#    - Per row cells
#      - button to trash bundle
# 4. Logout (we rely on SSO or BasicAUTH so only need a Logout function)
#
# For each activy there waybe both GET and POST reponses to handle.
#
# NOTE: Email retrieval and processing into DOI is handled automatically
# via a cronjob.  The Web UI only needs to manage actions on specific
# DOI.
#

@acacia.get('/add-doi')
def get_add_a_doi():
    '''Display the form to add a DOI'''
    person = person_from_environ(request.environ)
    logged_in = (person != None and person.uname != '')
    if not logged_in:
        redirect(f'/Shibboleth.sso/Logout')
    return page('form.tpl', title="Add DOI", uname = person.uname, form = 'add-doi')

@acacia.post('/add-doi')
def do_add_a_doi():
    '''Process submission of DOI and object URL'''
    error_message = None # Assume no errors to start.
# Get user info
    person = person_from_environ(request.environ)
    logged_in = (person != None and person.uname != '')
    if not logged_in:
        redirect(f'/Shibboleth.sso/Logout')
# Get form info
    uname = person.uname
    doi = request.forms.get("doi")
    object_url = request.forms.get("object_url")
    log(f'DEBUG (user: {uname}) doi: {doi} object_url: {object_url}')
# validate and save
    if validate_doi(doi):        
        # check if DOI already exists
        rec = Doi.get_or_none(Doi.doi == doi)
        if rec == None:
            # We're good, we can create a record
            rec, created = Doi.get_or_create(
                doi = doi,
                object_url = object_url,
                notes = f'Submitted by {person.display_name} via Acacia form.',
                m_from = f'{person.display_name} <{person.email}>')
        else:
            error_message = f'The DOI "{doi}" has previously been submitted.'
            return page('form.tpl', title="Doi previously submitted",
                uname = uname, doi = doi, object_url= object_url,
                error_message = error_message, form = 'doi-submitted')
    else:
        error_message = f'The DOI "{doi}" is not valid.'
        return page('form.tpl', title="Doi not valid",
                uname = uname, doi = doi, object_url= object_url,
                error_message = error_message, form = 'doi-submitted')
    return page('form.tpl', title="DOI Submitted", uname = uname,
        doi = doi, object_url = object_url, error_message = None, 
        form = 'doi-submitted')



@acacia.get('/messages')
@acacia.get('/messages/')
@acacia.get('/messages/<filter_by>')
@acacia.get('/messages/<filter_by>/<sort_by>')
def list_messages(filter_by = None, sort_by = None):
    ''' List the messages that have been retrieved for processing'''
    submit_email = config('SUBMIT_EMAIL', '')
    log(f'DEBUG list messsages, filter = {filter_by}, sort_by = {sort_by}')
    opts = []
    if filter_by:
        opts.append(filter_by)
    if sort_by:
        opts.append(sort_by)
    items = []
    for item in Message.select():
        items.append(item)
    description = f'''This is a list of all the emails retrieved from {submit_email}. You can manage those messages from your mail client.
'''
    return page('messages', title = 'Manage Messages', description = description, items = items, error_message = None)

@acacia.get('/message/<msg_id:int>')
def get_message(msg_id = None):
    '''Get the message record'''
    return '{}' # this would be a JSON object representing the message.


@acacia.get('/list')
@acacia.get('/list/')
@acacia.get('/list/<filter_by>')
@acacia.get('/list/<filter_by>/<sort_by>')
def list_items( filter_by = None, sort_by = None):
    ''' Process DOI should act on selections of list, it needs
        to trigger the generation of export bundles which are
        then emailed to the requesting librarian '''
    log(f'DEBUG List requested, filter = {filter_by}, sort_by = {sort_by}')
    opts = []
    if filter_by:
        opts.append(filter_by)
    if sort_by:
        opts.append(sort_by)
    #FIXME: need to apply options and describe 
    items = []
    for item in Doi.select():
        items.append(item)
    description = f'''This is a list of DOIs that Acacia knows about.''' # FIXME: Add information about sorts and filter here and workflow
    return page('list', title = 'Manage DOI', description = description, items = items)

@acacia.get('/eprint-xml/<rec_id:int>')
def get_eprint_xml(rec_id = None):
    '''Retrieve the EPrint XML saved as "metadata" in the doi object'''
    rec = Doi.get_by_id(str(rec_id))
    if rec != None:
        return xml_page(data = '''<?xml version='1.0' encoding='utf-8'?>''' + "\n" + rec.metadata, content_type = 'text/plain')
    return page('error', title = "EPrint XML", summary = 'access error',
                message = ('EPrint XML not available'))

@acacia.get('/item/<rec_id:int>')
def get_status(rec_id = None):
    '''JSON response of individual object, used to update status such as bundle ready'''
    return '{}' # This would be a JSON object representing updates to a row



# Error pages.
# .........................................................................
# NOTE: the Bottle session plugin does not seem to supply session arg
# to @error.
#

@acacia.get('/notallowed')
@acacia.post('/notallowed')
def not_allowed():
    return page('error', summary = 'access error',
                message = ('The requested page does not exist or you do not '
                           'not have permission to access the requested item.'))

@acacia.error(404)
def error404(error):
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('404', title = 'Acacia Error', code = error.status_code, message = error.body)


@acacia.error(405)
def error405(error):
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('error', title = "Acacia Error", summary = 'method not allowed',
                message = ('The requested method does not exist or you do not '
                           'not have permission to perform the action.'))


#
# Static web pages needed in Web UI
# ........................................................................
#

@acacia.get('/') 
def dashboard():
    '''Manage provides a dashbaord of available activities.'''
# Load static dashboard page
    return static_file('dashboard.html', root = os.path.join(_SERVER_ROOT, 'htdocs'))


@acacia.get('/about')
@acacia.get('/about/')
def manage_items():
    '''Manage provides a dashbaord of available activities.'''
# Load static dashboard page
    return static_file('about.html', root = os.path.join(_SERVER_ROOT, 'htdocs'))


@acacia.get('/favicon.ico')
def favicon():
    '''Return the favicon.'''
    return static_file('favicon.ico', root = os.path.join(_SERVER_ROOT, 'htdocs/media'))


# Handle our static accets in htdocs/css, htdocs/assets, htdocs/media, htdocs/help
@acacia.get('/<folder:re:(assets|css|about|media|help)>/')
@acacia.get('/<folder:re:(assets|css|about|media|help)>/<filename:re:[-a-zA-Z0-9]+.(gif|ico|png|jpg|svg|css|js|html|md)>')
def include_file(folder, filename = 'index.html'):
    '''Return a static file'''
    p = os.path.join(_SERVER_ROOT, 'htdocs', folder)
    log(f'returning {folder} file {filename} {p}')
    return static_file(filename, root = p)
