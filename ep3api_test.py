#!/usr/bin/env python3
'''
ep3api_test.py tests the ep3api.py python library used in acacia object.
'''
from cltests import TestSet, T, IsSuccessful
from ep3api import Ep3API


api = Ep3API('http://localhost:8484', 'lemurprints')
print(f'DEBUG url: {api.url}')
print(f'DEBUG repo_id: {api.repo_id}')

def test_eprint_lists():
    t = T()
    keys, err = api.keys()
    t.Expected(None, err, "Did not expect an error for keys")
    t.Expected(True, keys != None, "Should have a list of keys")
    return t.Results()

if __name__ == '__main__':
    ts = TestSet("ep3api_test")
    ts.add(test_eprint_lists)
    IsSuccessful(ts.run())




