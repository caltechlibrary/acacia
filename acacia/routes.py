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
from datetime import datetime
import json

from decouple import config

import bottle
from   bottle import Bottle, HTTPResponse, static_file, template
from   bottle import request, response, redirect, route, get, post, error

from . import __app__, __version__, __description__, __author__, __license__, __url__, __email__

# Acacia Code
from .persons import Person, person_from_environ
from .messages import Message, EMailProcessor
from .doi import Workflow, Doi, DOIProcessor, validate_doi, __doi2eprintxml_version__
from .ep3apid import Ep3API

if __debug__:
    from sidetrack import set_debug, log


# General configuration and initialization.
# .............................................................................

# Begin by creating a Bottle object on which we will define routes and other
# behaviors in the rest of this file.
acacia = Bottle()

repo_id = config('REPO_ID', 'caltechauthors')
ep3apid_url = config('EP3APID_URL', 'http://localhost:8484')
ep3api = Ep3API(ep3apid_url, repo_id)

# Get version numbers for doi2eprintxml and ep3apid
__ep3apid_version__ = ep3api.version()


#
# FIXME: Setup access to ep3apid via acacia/ep3api.py
#

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

def page(name, person, **kargs):
    '''Create a page using template "name" with some standard variables set.'''
#FIXME: we're allowing person_from_environ multiple times per request,
# maybe this should happend once in a bottle plugin and all requests
# should have a person object or person as None.
    logged_in = (person != None and person.uname != '')
    staff_user = person.has_role(['admin', 'editor'])
    if kargs.get('browser_no_cache', False):
        response.add_header('Expires', '0')
        response.add_header('Pragma', 'no-cache')
        response.add_header('Cache-Control',
                            'no-store, max-age=0, no-cache, must-revalidate')
    return template(name, base_url = acacia.base_url, version = __version__,
                    person = person,
                    logged_in = logged_in, staff_user = staff_user,
                    help_url = _HELP_URL, **kargs)

def json_page(data, **kargs):
    content_type = 'application/json'
    content_type = kargs.get('content_type', 'application/json')
    response.add_header('Content-Type', content_type)
    return data

def xml_page(data, **kargs):
    content_type = 'application/xml'
    content_type = kargs.get('content_type', 'application/xml')
    response.add_header('Content-Type', content_type)
    return data

def debug_mode():
    '''Return True if we're running Bottle's default server in debug mode.'''
    return getattr(acacia, 'debug_mode', False)


def required_roles(person):
    allowed_roles = [ 'admin', 'editor' ]
    logged_in = (person != None and person.uname != '')
    if not logged_in:
        redirect(f'{acacia.base_url}/logout')
    for role in allowed_roles:
        if person.has_role(role):
            return
    redirect(f'{acacia.base_url}/notallowed')

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

@acacia.get('/whoami')
def whoami():
    person = person_from_environ(request.environ)
    if 'REMOTE_USER' in request.environ:
        shib_user = request.environ['REMOTE_USER']
    else:
        shib_user = ''
    return page('whoami.tpl', person, title='Who am I?', description = 'A page for debugging user/role issues', shib_user = shib_user)

@acacia.get('/add-doi')
def get_add_a_doi():
    '''Display the form to add a DOI'''
    person = person_from_environ(request.environ)
    required_roles(person)
    logged_in = (person != None and person.uname != '')
    if not logged_in:
        redirect(f'/Shibboleth.sso/Logout')
    return page('form.tpl', person, title="Add DOI", uname = person.uname, form = 'add-doi')

@acacia.post('/add-doi')
def do_add_a_doi():
    '''Process submission of DOI and object URL'''
    person = person_from_environ(request.environ)
    required_roles(person)
    error_message = None # Assume no errors to start.
    uname = person.uname
    doi = request.forms.get("doi")
    object_url = request.forms.get("object_url")
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
            return page('form.tpl', person, title="Doi previously submitted",
                uname = uname, doi = doi, object_url= object_url,
                error_message = error_message, form = 'doi-submitted')
    else:
        error_message = f'The DOI "{doi}" is not valid.'
        return page('form.tpl', person, title="Doi not valid",
                uname = uname, doi = doi, object_url= object_url,
                error_message = error_message, form = 'doi-submitted')
    return page('form.tpl', person, title="DOI Submitted", uname = uname,
        doi = doi, object_url = object_url, error_message = None, 
        form = 'doi-submitted')


@acacia.get('/get-messages')
def get_messages():
    person = person_from_environ(request.environ)
    required_roles(person)
    mail_processor = EMailProcessor()
    if mail_processor.get_mail():
        redirect(f'{acacia.base_url}/messages')
    return page('error', person, title="Get Messages", summary = "Error retrieving EMAIL submissions", description = (
        f'EMail account: {mail_processor.email}',
        f'SMTP hostname: {mail_processor.smtp_host}'))

@acacia.get('/messages-to-doi')
def message_to_doi():
    person = person_from_environ(request.environ)
    required_roles(person)
    mail_processor = EMailProcessor()
    doi_processor = DOIProcessor()
    records = mail_processor.get_unprocessed()
    if len(records) == 0:
        redirect(f'{acacia.base_url}/manage-doi/')
    errors = []
    err_cnt, item_cnt, doi_cnt = 0, 0, 0
    for rec in records:
        n, e_cnt, err = doi_processor.message_to_doi(rec)
        if err:
            errors.append(f'{err}')
            err_cnt += e_cnt
        else:
            rec.m_processed = True
            rec.save()
        doi_cnt += n
        item_cnt += 1
    if err_cnt == 0:
        redirect(f'{acacia.base_url}/manage-doi/')
    return page('error', person, title='Messages to DOI', summary = "Error converting email messages into DOI records", description = (f'''{errors.join(" ")}'''))


@acacia.get('/message-reset/<rec_id:int>')
def message_reset(rec_id = None):
    person = person_from_environ(request.environ)
    required_roles(person)
    if rec_id != None:
        record = Message.get_by_id(str(rec_id))
        if record != None:
            record.m_processed = False
            record.save()
    redirect(f'{acacia.base_url}/messages')

@acacia.get('/message-remove/<rec_id:int>')
def message_remove(rec_id = None):
    person = person_from_environ(request.environ)
    required_roles(person)
    if rec_id != None:
        rec = Message.get_by_id(str(rec_id))
        if rec != None:
            query = Message.delete().where(Message.id == rec_id)
            query.execute()
        redirect(f'{acacia.base_url}/messages/')
    else:
        return page('error', person, title='Delete Message', summary ='deletion failed', message = (f'Message {rec_id} not found'))
    return page('error', person, title='Delete Message', summary ='deletion failed', message = (f'Missing record ID in URL'))


@acacia.get('/retrieve-metadata')
@acacia.get('/retrieve-metadata/')
@acacia.get('/retrieve-metadata/<rec_id:int>')
def get_metadata(rec_id = None):
    person = person_from_environ(request.environ)
    required_roles(person)
    doi_processor = DOIProcessor()
    errors = []
    if rec_id == None:
        records = doi_processor.get_unprocessed()
        if len(records) > 0:
            err_cnt, item_cnt, doi_cnt = 0, 0, 0
            for record in records:
                now = datetime.now()
                if record.status != 'ready' or not record.metadata:
                    src, err = doi_processor.get_metadata(record.doi)
                    if err:
                        msg = f'ERROR get_metadata({record.doi}) {now.isoformat()}: {err}'
                        errors.append(msg)
                        err_cnt += 1
                        record.status = 'processing_error'
                        record.notes += msg + "\n"
                        record.updated = now
                    else:
                        record.metadata = src
                        record.status = 'ready'
                        record.updated = now
                        doi_cnt += 1
                if not record.eprint_id:
                    eprint_id, err = None,None # DEBUG
                    ids, err = ep3api.doi(record.doi)
                    if err:
                        msg = f'ERROR ep3api.doi({record.doi}): {err}'
                        errors.append(msg)
                        record.status = 'processing_error'
                        record.notes += msg + "\n"
                        record.updated = now
                        err_cnt += 1
                    elif ids != None and len(ids) > 0:
                        eprint_id = ids[0]
                        record.repo_id = repo_id
                        record.eprint_id = eprint_id
                    record.save()
                item_cnt += 1
            if err_cnt == 0:
                redirect(f'{acacia.base_url}/manage-doi')
    else:
        now = datetime.now()
        record = Doi.get_or_none(Doi.id == str(rec_id))
        if record != None:
            metadata, err = doi_processor.get_metadata(record.doi)
            if err:
                msg = f'ERROR get_metadata({record.doi}) {now.isoformat}: {err}'
                errors.append(msg)
                record.status = 'processing_error'
                record.notes += msg + "\n"
                record.updated = now
            else:
                record.repo_id = repo_id
                record.metadata = metadata
                record.status = 'ready'
                record.updated = now
            if not record.eprint_id:
                eprint_id, err = None,None # DEBUG
                ids, err = ep3api.doi(record.doi)
                if err:
                    msg = f'ERROR ep3api.doi({record.doi}): {err}'
                    errors.append(msg)
                    record.status = 'processing_error'
                    record.notes += msg + "\n"
                    record.updated = now
                elif ids != None and len(ids) > 0:
                    eprint_id = ids[0]
                    record.repo_id = repo_id
                    record.eprint_id = eprint_id
            record.save()
        else:
            errors.append('record not found in DOI table')
    if len(errors) > 0:
        return page('error', person, title = 'Retrieve Metadata',
            summary = 'Error retrieving metadata', description = errors, message = errors) 
    redirect(f'{acacia.base_url}/manage-doi')
        

@acacia.get('/messages')
@acacia.get('/messages/')
@acacia.get('/messages/<filter_by>')
@acacia.get('/messages/<filter_by>/<sort_by>')
def list_messages(filter_by = None, sort_by = None):
    ''' List the messages that have been retrieved for processing'''
    person = person_from_environ(request.environ)
    required_roles(person)
    submit_email = config('SUBMIT_EMAIL', '')
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
    return page('messages', person, title = 'Manage Messages', description = description, items = items, error_message = None)


@acacia.get('/manage-doi')
@acacia.get('/manage-doi/')
@acacia.get('/manage-doi/<filter_by>')
@acacia.get('/manage-doi/<filter_by>/<sort_by>')
def list_items( filter_by = None, sort_by = None):
    ''' Process DOI should act on selections of list, it needs
        to trigger the generation of export bundles which are
        then emailed to the requesting librarian '''
    view_url = config('VIEW_URL', '')
    person = person_from_environ(request.environ)
    required_roles(person)
    opts = []
    if filter_by:
        opts.append(filter_by)
    if sort_by:
        opts.append(sort_by)
    #FIXME: need to apply options and describe 
    items = []
    for item in Doi.select():
        if item.doi != None and not item.eprint_id:
            ids, err = ep3api.doi(item.doi)
            if err == None and ids != None and len(ids) > 0:
                item.eprint_id = ids[0]
        items.append(item)
    description = f'''
This is a list of DOIs that Acacia knows about.
'''
    return page('manage-doi', person, title = 'Manage DOI', description = description, items = items, repo_id = repo_id, view_url = view_url)

@acacia.get('/eprint-xml/<rec_id:int>')
def get_eprint_xml(rec_id = None):
    '''Retrieve the EPrint XML saved as "metadata" in the doi object'''
    person = person_from_environ(request.environ)
    required_roles(person)
    rec = Doi.get_by_id(str(rec_id))
    if rec != None:
        return xml_page(data = '''<?xml version='1.0' encoding='utf-8'?>''' + "\n" + rec.metadata, content_type = 'text/plain')
    return page('error', person, title = "EPrint XML", summary = 'access error',
                message = ('EPrint XML not available'))

@acacia.get('/viewer-json/<rec_id:int>')
def get_viewer_json(rec_id = None):
    '''Retrieve the JSON data needed by the viewer widget.'''
    person = person_from_environ(request.environ)
    required_roles(person)
    rec = Doi.get_by_id(str(rec_id))
    if rec != None:
        obj = (json.loads(rec.metadata))
        if ('eprint' in obj) and (len(obj['eprint']) > 0):
            return json_page(obj['eprint'][0])
    return page('error', person, title = "Viewer JSON", summary = 'access error',
                message = ('object not found'))


@acacia.get('/viewer/<rec_id:int>')
def get_viewer(rec_id = None):
    '''Retrieve the converted CrossRef/DataCite record and display it as an EPrints record.'''
    person = person_from_environ(request.environ)
    required_roles(person)
    rec = Doi.get_by_id(str(rec_id))
    description = f'''
This is a view of the record before import.
'''
    if (rec != None):
        return page('viewer', person, title = "View Record", description = description, rec_id = rec_id)
    return page('error', person, title = "View Record", summary = 'access error',
                message = ('View record not available'))

@acacia.get('/doi-reset/<rec_id:int>')
def doi_reset(rec_id = None):
    person = person_from_environ(request.environ)
    required_roles(person)

    if rec_id != None:
        record = Doi.get_by_id(str(rec_id))
        if record != None:
            record.metadata = ""
            record.status = 'unprocessed'
            record.save()
    redirect(f'{acacia.base_url}/manage-doi/')

@acacia.get('/doi-remove/<rec_id:int>')
def doi_remove(rec_id = None):
    '''Remove the requested record'''
    person = person_from_environ(request.environ)
    required_roles(person)
    base_url = config('BASE_URL', '')
    if rec_id != None:
        rec = Doi.get_by_id(str(rec_id))
        if rec != None:
            query = Doi.delete().where(Doi.id == rec_id)
            query.execute()
        redirect(f'{acacia.base_url}/manage-doi')
    else:
        return page('error', person, title='Delete request', summary ='deletion failed', message = (f'Record {rec_id} not found'))
    return page('error', person, title='Delete request', summary ='deletion failed', message = (f'Missing record ID in URL'))

@acacia.get('/item-import/<rec_id:int>')
def item_import(rec_id = None):
    '''Import an Acacia record into the IR (e.g. CaltechAUTHORS)'''
    person = person_from_environ(request.environ)
    required_roles(person)
    base_url = config('BASE_URL', '')
    if rec_id != None:
        rec = Doi.get_by_id(str(rec_id))
        if rec != None and not rec.eprint_id:
            src = rec.metadata
            if not isinstance(src, bytes):
                src = src.encode('utf-8')
            ids, err = ep3api.eprint_import(person.userid, src)
            if err:
                return page('error', person, title = "Import EPrint", summary = 'failed to import to eprints', message = err)
            if ids != None and len(ids) > 0:
                rec.eprint_id = ids[0]
                rec.status = 'imported'
                rec.save()
    redirect(f'{acacia.base_url}/manage-doi')

@acacia.get('/eprint-json/<rec_id:int>')
def get_eprint_json(rec_id = None):
    '''Retrieve the EPrint JSON from repository and display it.'''
    person = person_from_environ(request.environ)
    required_roles(person)
    rec, err = ep3api.eprint(str(rec_id))
    if err:
        return page('error', person, title = "EPrint JSON", summary = 'access error', message = err)
    if rec == None:
        return page('error', person, title = "EPrint JSON", summary = 'access error', message = ('EPrint JSON not available'))
    return json_page(data = json.dumps(rec, sort_keys = True, indent = 4))

@acacia.get('/version')
def get_version():
    obj = {
        "application": __app__,
        "version": __version__,
        "description": __description__,
        "url": __url__,
        "authors": __author__,
        "email": __email__, 
        "license": __license__,
        "depends_on": []
    }
    # Get ep3apid version number
    obj["depends_on"].append(__ep3apid_version__)
    obj["depends_on"].append(__doi2eprintxml_version__)
    # Get doi2eprintxml version number
    return json_page(data = json.dumps(obj, sort_keys = True, indent = 4))


# Error pages.
# .........................................................................
# NOTE: the Bottle session plugin does not seem to supply session arg
# to @error.
#

@acacia.get('/notallowed')
@acacia.post('/notallowed')
def not_allowed():
    person = person_from_environ(request.environ)
    return page('error', person, title = 'Unauthorized', summary = 'access error',
                message = ('The requested page does not exist or you do not '
                           'not have permission to access the requested item.'))

@acacia.error(404)
def error404(error):
    person = person_from_environ(request.environ)
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('404', person, title = 'Acacia Error', code = error.status_code, message = error.body)


@acacia.error(405)
def error405(error):
    person = person_from_environ(request.environ)
    log(f'{request.method} called on {request.path}, resulting in {error}')
    return page('error', person, title = "Acacia Error", summary = 'method not allowed',
                message = ('The requested method does not exist or you do not '
                           'not have permission to perform the action.'))


#
# Static web pages needed in Web UI
# ........................................................................
#

@acacia.get('/') 
def home_page():
    '''Manage provides a dashbaord of available activities.'''
    person = person_from_environ(request.environ)
    required_roles(person)
# Load static dashboard page
    return static_file('index.html', root = os.path.join(_SERVER_ROOT, 'htdocs'))


@acacia.get('/about')
@acacia.get('/about/')
def manage_items():
    person = person_from_environ(request.environ)
    required_roles(person)
    '''Manage provides a dashbaord of available activities.'''
# Load static dashboard page
    return static_file('about.html', root = os.path.join(_SERVER_ROOT, 'htdocs'))



@acacia.get('/favicon.ico')
def favicon():
    '''Return the favicon.'''
    return static_file('favicon.ico', root = os.path.join(_SERVER_ROOT, 'htdocs/media'))


# Handle our help pages
@acacia.get('/help')
@acacia.get('/help/')
@acacia.get('/help/<filename:re:[-a-zA-Z0-9]+.(gif|ico|png|jpg|svg|html|md)>')
def help_pages(filename = 'index.html'):
    '''Return a static file'''
    person = person_from_environ(request.environ)
    required_roles(person)
    p = os.path.join(_SERVER_ROOT, 'htdocs', 'help')
    log(f'returning help file {filename} {p}')
    return static_file(filename, root = p)


# Handle our static accets in htdocs/css, htdocs/assets, htdocs/media
@acacia.get('/<folder:re:(assets|css|about|media|widgets)>/')
@acacia.get('/<folder:re:(assets|css|about|media|widgets)>/<filename:re:[-a-zA-Z0-9]+.(gif|ico|png|jpg|svg|css|js|html|md)>')
def include_file(folder, filename = 'index.html'):
    '''Return a static file'''
    p = os.path.join(_SERVER_ROOT, 'htdocs', folder)
    log(f'returning {folder} file {filename} {p}')
    return static_file(filename, root = p)


