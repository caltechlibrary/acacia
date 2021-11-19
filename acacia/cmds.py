'''
cmds.py a light weight wrapper around Popen and PIPES so our
cli interactions are handled in a consistant manner.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

#
# Handle HTTP Requests
#
from urllib import request

def http_get(u):
    '''http_get takes a URL and performs a GET. It returns a touple of payload and error'''
    req = request.Request(u)
    try:
        res = request.urlopen(req)
    except HTTPError as e:
        return '', f'{e.code}, {e.reason}'
    except URLError as e:
        return '', f'{e.reason}'
    else:
        return res.read(), None
    

#
# Run OS commands capturing output and error
#
from subprocess import Popen, PIPE, run

def run(cmd):
    '''run uses Popen to run a command and capture it's stdout and stderr
       returns two values out holds the what was sent to stdout, err holds
       what was sent to stderr. Note some cli use stderr by default'''
    out, err = None, None
    with Popen(cmd, stdout = PIPE, stderr = PIPE) as proc:
        err = proc.stderr.read().strip().decode('utf-8')
        if err == '':
            err = None
        out = proc.stdout.read().strip().decode('utf-8')
        if out == '':
            out = None
    return out, err


def http_get(url):
    '''Return get results as a tuple of src and error'''

def http_post(url, data):
    '''Return POST "data" and returns as a tuple of src and error'''

