from _db import *
gdb=gus_database();           
                        
def test_truncate_all():
        print "--------------TRUNCATE ALL TABLES ALL TESTS DONE!---------------"
        gdb.db.truncate('gus_users')
        gdb.db.truncate('gus_groups')
        gdb.db.truncate('associated')
        gdb.db.truncate('gus_roles')

def test_member_create(users):
        print "--------------MEMBER ADD TESTS START---------------"
         
        for i in range(0,len(users)):
                if(gdb.add_user(users[i]['n'],users[i]['p'],users[i]['e'])):
                        print "ADDED "+users[i]['n']
                else:
                        print gdb.error_msg
        print "--------------MEMBER ADD TESTS DONE---------------"

def test_group_create(groups):
        print "--------------GROUP ADD TESTS START---------------"
         
        for i in range(0,len(groups)):
                if(gdb.create_group(groups[i]['n'],groups[i]['o'])):
                        print "Created Group :"+groups[i]['n']
                else:
                        print gdb.error_msg
        print "--------------GROUP ADD TESTS DONE---------------"
def test_associations():
        print "--------------GROUP ASSOC TESTS START---------------"
        #first lets create some more members
        test_member_create(
                [{'n':'Joran5','e':'joranbeasleyxx@gmail.com','p':'password'},
                 {'n':'Joran6','e':'joranbeasley11@gmail.com','p':'password'},
                 {'n':'Joran7','e':'joranbeasley22@gmail.com','p':'password'},
                 {'n':'Joran8','e':'joranbeasley32@gmail.com','p':'password'},
                 {'n':'goodemail','e':'bad@email.net','p':'password'}]
                )
        for i in range(1,10):
                uid=randint(1,7)#random 1..7
                gid=randint(1,2)#random 1 or 2
                if( gdb.set_role(uid,gid,i)):
                        print "Associated USER(%d) with GROUP(%d) having ROLE(%d)"%(uid,gid,i) 
                else:
                        print gdb.error_msg
                
        print "--------------GROUP ASSOC TESTS DONE---------------"
def test_group_retrieval():
        print "--------------GROUP RETRIEVAL TESTS START---------------"
        for i in range(1,3):
                print "  -- Members of (%d) --"%(i)
                M=gdb.get_group_members(i)
                for j in range(0,len(M)):
                        print M[j]
        print "--------------GROUP RETRIEVAL TESTS END---------------"
def test_member_retrieval():
        print "--------------GROUP RETRIEVAL TESTS START---------------"
        for i in range(1,8):
                print "  -- Groups of USER(%d) --"%(i)
                M=gdb.get_members_groups(i)
                for j in range(0,len(M)):
                        print M[j]
        print "--------------GROUP RETRIEVAL TESTS END---------------"
def test_group_delete():
        print "--------------GROUP DELETE TESTS START---------------"
        for i in range(1,4):
                print "DELETING %d"%i
                if(gdb.del_group(i)):
                        print "  DELETED GROUP %d"%i
                else:
                        print "  ERROR NOTHING DELETED"
        test_group_retrieval()
        test_member_retrieval()
        print "--------------GROUP RETRIEVAL TESTS END---------------"
def test_user_delete():
        print "--------------MEMBER DELETE TESTS START---------------"
        for i in range(1,9):
                print "DELETING USER %d"%i
                if(gdb.del_user(i)):
                        print "  DELETED USER %d"%i
                else:
                        print "  ERROR NO USER DELETED"
        print "--------------MEMBER RETRIEVAL TESTS END---------------"
def test_db():
        print "********************Test Database Functionality**************"
        test_member_create(
                [{'n':'Joran1','e':'joranbeasley@gmail.com','p':'password'},
                 {'n':'Joran2','e':'joranbeasley1@gmail.com','p':'password'},
                 {'n':'Joran3','e':'joranbeasley@gmail.com','p':'password'},#dupe email should fail
                 {'n':'Joran1','e':'joranbeasley2@gmail.com','p':'password'},#dupe username should fail
                 {'n':'bademail','e':'bad@email','p':'password'}]#bad email
                )
        test_group_create([{'n':'J Group1','o':'1'},{'n':'J Group2','o':'2'}])
        test_associations()
        test_group_retrieval()
        test_member_retrieval()
        test_group_delete()
        test_user_delete()
        test_truncate_all()

test_db();
