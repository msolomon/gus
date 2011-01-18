# Sasha Kopriva
# remove user test case
# 11/10/2010

from groups import *
from sys import stderr

def testcase_removeuser():
    member1 = Member('matrim', 'email')
    member2 = Member('moiraine', 'email')
    member3 = Member('perrin', 'email')
    member4 = Member('lanfear', 'email')

    users = [member1, member2, member3, member4]

    group1 = Group('Group1', member2)
    group1.add_member(member1)
    group1.add_member(member2)
    group1.add_member(member3)

    print 'Test Remove Member:'
    print '-'*20
    print [member.username for member in group1.members]
    for user in users:
        print
        print 'Remove Member %s : %s' % (user, group1.remove_member(user))
        print [member.username for member in group1.members]

testcase_removeuser()
