#!/usr/bin/env python3
'''
success_test.py implements an example test which should exit with
process value of zero (success) and display "OK, success_test".
'''

from cltests import TestSet, T, IsSuccessful

def test1():
    t = T()
    t.Expected(True, True, "True should equal True")
    return t.Results()

def test2():
    a, b = [1, 2, 3, 4], [1, 2, 3, 4]
    t = T()
    t.ExpectedList(a, b, "list a should equal list b")
    return t.Results()

if __name__ == '__main__':
    ts = TestSet("success_test")
    ts.add(test1)
    ts.add(test2)
    IsSuccessful(ts.run())

