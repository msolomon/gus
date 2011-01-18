from groups import *
from sys import stderr

def AddUserTest():
    print("Group members should output:")
    outA = "Bob's Group:\tOwner: Bob\n\tMembers: ['Bob']"
    print(outA)
    print('\n')
    outB = "Bob's Group:\tOwner: Bob\n\tMembers: ['Bob', 'Joe']"
    print(outB)
    print('\n')
    outC = "Bob's Group:\tOwner: Bob\n\tMembers: ['Bob', 'Joe', 'Bill']"
    print(outC)
    print('\n')
    print("********************************************")
    print("Actual Output:")
    people = []
    people.append(Member('Bob', 'bob@uidaho.edu'))
    people.append(Member('Joe', 'joe@uidaho.edu'))
    people.append(Member('Bill', 'bill@uidaho.edu'))
    group = Group("Bob's Group", people[0])
    inA = "%s:\tOwner: %s\n\tMembers: %s" % (group, group.owner, [member.username for member in group.members])
    print(inA)
    print('\n')
    group.add_member(people[1])
    inB = "%s:\tOwner: %s\n\tMembers: %s" % (group, group.owner, [member.username for member in group.members])
    print(inB)
    print('\n')
    group.add_member(people[2])
    inC = "%s:\tOwner: %s\n\tMembers: %s" % (group, group.owner, [member.username for member in group.members])
    print(inC)
