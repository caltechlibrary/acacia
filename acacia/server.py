'''
server.py: Acacia server definition.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''
import os

import bottle
from   bottle import Bottle, HTTPResponse, static_file, template
from   bottle import request, response, redirect, route, get, post, error

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
_SERVER_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))

# Tell Bottle where to find templates.  This is necessary for both the Bottle
# template() command to work and also to get %include to work inside our .tpl
# template files.  Rather surprisingly, the only way to tell Bottle where to
# find the templates is to set this Bottle package-level variable.
bottle.TEMPLATE_PATH.append(os.path.join(_SERVER_ROOT, 'templates'))



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

@acacia.get('/list')
@acacia.get('/list/<filter_by>')
@acacia.get('/list/<filter_by>/<sort_by>')
def get_list(filter_by = None, sort_by = None, msg = None):
    '''Display a list of DOIs to be processed further.'''
    items = [] # DEBUG need to build an item list here.
    return page('list', items = items, msg = None, content = content)

@acacia.post('/list')
@acacia.get('/list/<filter_by>')
@acacia.get('/list/<filter_by>/<sort_by>')
def process_list( filter_by = None, sort_by = None):
    ''' Process DOI should act on selections of list, it needs
        to trigger the generation of export bundles which are
        then emailed to the requesting librarian '''
    opts, options = [], ''
    if filter_by:
        opts.append(filter_by)
    if sort_by:
        opts.append(sort_by)
    if len(opts) > 0:
        options = '/' + '/'.join(opts)
    return redirect(f'/list{options}', msg = "processed")

@acacia.get('/status/<rec_id:int>')
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
    return page('404', code = error.status_code, message = error.body)


@acacia.error(405)
def error405(error):
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('error', summary = 'method not allowed',
                message = ('The requested method does not exist or you do not '
                           'not have permission to perform the action.'))


#
# Static web pages needed in Web UI
# ........................................................................
#

@acacia.get('/') 
@acacia.get('/dashbord')
def manage_items():
    '''Manage provides a dashbaord of available activities.'''
# Load static dashboard page
    return static_file('dashboard.html', root = os.path.join(_SERVER_ROOT, 'htdocsa'))

@acacia.get('/about')
def general_page(name = '/'):
    '''Display the About page.'''
    return static_file('about.html', root = os.path.join(_SERVER_ROOT, 'htdocs'))

@acacia.get('/favicon.ico')
def favicon():
    '''Return the favicon.'''
    return static_file('favicon.ico', root = os.path.join(_SERVER_ROOT, 'htdocs/media'))

@acacia.get('/media/<filename:re:[-a-zA-Z0-9]+.(ico|png|jpg|svg)>')
def include_file(filename):
    '''Return a static file'''
    p = os.path.join(_SERVER_ROOT, 'htdocs', 'media')
    log(f'returning media file {filename} {p}')
    return static_file(filename, root = p)

@acacia.get('/assets/<filename:re:[-a-zA-Z0-9]+.(gif|png|jpg|svg)>')
def included_assets_file(filename):
    '''Return a static file used with %include in a template.'''
    p = os.path.join(_SERVER_ROOT, 'htdocs', 'assets')
    log(f'returning assets file {filename} {p}')
    return static_file(filename, root = p)

@acacia.get('/css/<filename:re:[-a-zA-Z0-9]+.(css)>')
def included_css_file(filename):
    '''Return a static file used with %include in a template.'''
    p = os.path.join(_SERVER_ROOT, 'htdocs', 'css')
    log(f'returning CSS file {filename} {p}')
    return static_file(filename, root = p)

