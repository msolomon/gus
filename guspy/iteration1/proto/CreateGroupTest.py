#CreateGroupTest by Max Stillwell - Nov 10, 2010

from groups import *

def CreateGroupTest():
    #Expected Output
    EOutput = "0's Group:\n Owner: 0\n1's Group:\n Owner: 1\n2's Group:\n Owner: 2\n3's Group:\n Owner: 3\n4's Group:\n Owner: 4\n"

    print("Expected Output:\n%s\n" % EOutput)

    #Actual Output
    Users = []
    AOutput = ""
    Groups = []
    
    for UName in ['0', '1', '2', '3', '4']:
        Users.append(Member(UName, 'pass', '%s@uidaho.edu' % UName))
    
    for GName in Users:
        group = Group("%s's Group" % GName.username, GName)
        Groups.append(group)

    for g in Groups:
        AOutput += ("%s:\n Owner: %s\n" % (g.name, g.owner))

    print("Actual Output:\n%s\n" % AOutput)

    #Pass/Fail?
    if EOutput == AOutput:
        print("Pass")
    else:
        print("Fail")
#END

#if __name__ == '__main__':
#    CreateGroupTest()
#END
