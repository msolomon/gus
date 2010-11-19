# Mike Solomon
# 11/9/10

from groups import *
from sys import stderr

def testcase_changeowner():
    alice = Member('alice', 'alice@uidaho.edu')
    bob = Member('bob', 'alice@uidaho.edu')
    chad = Member('chad', 'chad@uidaho.edu')

    users = [bob, chad, alice]

    a = Group('A', alice)

    print 'Testing Change Owner:'
    print '-' * 40
    for user in users:
        print 'Group %s owner: %s' % (a, a.owner)
        print 'Changing to %s...' % (user)
        a.owner = user
        print 'Group %s new owner: %s' % (a, a.owner)
        if a.owner == user:
            print 'PASS\n'
        else:
            print >> stderr, 'FAIL\n'

if __name__ == '__main__':
    testcase_changeowner()
