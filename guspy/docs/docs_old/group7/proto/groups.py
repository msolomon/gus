from hashlib import sha1
from random import getrandbits

class Member(object):
    userID=-1
    def __str__(self):
        return self.username
  
    def __init__(self, username, email):
        self.username = username
        #self.change_password(password)
        self.email = email
        self.groups = set()
 

    def change_password(self, password):
        self.salt = hex(getrandbits(64))
        self.passhash = sha1(password + self.salt).hexdigest()

 
    def leave_group(self, group):
        # in reality we'd not return a status string
        if self == group.owner:
            return "can't leave as owner"
        try:
            group.members.remove(self)
            self.groups.remove(group)
        except:
            return "not in group"
        return "removed"
 
 
class Group(object):
    groupID = -1
    def __str__(self):
        return self.name
 
    def __init__(self, name, owner):       
        self.name = name
        self.owner = owner
        self.members = set([owner])
 
    def add_member(self, member):
        member.groups.add(self)
        self.members.add(member)
 
    def remove_member(self, member):
        # in reality we'd not return a status string
        if member == self.owner:
            return "can't remove owner"
        try:
            member.groups.remove(self)
            self.members.remove(member)
        except:
            return "member not in group"
        return "removed"
    def empty_group(self):
        for member in [m for m in self.members]:
             self.remove_member(member)

 
