#!/usr/bin/env python3
'''
success_test.py implements an example test which should exit with
process value of zero (success) and display "OK, success_test".
'''

from cltests import TestSet, T, IsSuccessful

def test1():
    t = T()
    t.Expected(True, False, "True does not equal False")
    return t.Results()

def test2():
    a, b = [1, 2, 3, 4], [1, 6, 7]
    t = T()
    t.ExpectedList(a, b, "list a length is not equal to list b")
    a, b = [1, 2, 3, 4], [1, 6, 7, 4]
    t.ExpectedList(a, b, "list a value are not  equal to list b")
    return t.Results()

if __name__ == '__main__':
    print(f'NOTE: This test should fail twice exit')
    print(f'The exit code should not be zero.')
    ts = TestSet("fail_test")
    ts.add(test1)
    ts.add(test2)
    IsSuccessful(ts.run())

