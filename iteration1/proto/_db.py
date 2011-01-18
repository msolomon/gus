import _mysql
import re
from hashlib import sha1
from random import *
from groups import Member,Group
class db:  #underlying base connection
        #connection info this should probably be loaded from external file
        HOST="localhost"
        USER="root"
        PASS=""
        NAME="gus"
        
        def __init__(self):
                self.sql_error=""
                
        #open connection                
        def dbopen(self):
                self.db_inst = _mysql.connect(self.HOST,self.USER,self.PASS,self.NAME)
        
        #mysql_real_escape string
        def dbescape(self,string1):
                return _mysql.escape_string(string1)
        #pass query and generate result information     
        def dbquery(self,query):
                self.db_inst.query(""+query+"")
               
        #close connection
        def dbclose(self):
                self.db_inst.close()

                        

class database: # slightly refined version with helper functions
        DB=db()
        last_query=None
        def dbquery(self,Query):
                #//print Query
                self.last_query = Query
                self.DB.dbopen()
                self.result = []
                try :
                    self.DB.dbquery(Query)
                except _mysql.Error,e:
                    self.sql_error = e
                    return False
                self.sql_affected_ct = self.DB.db_inst.affected_rows()
                self.sql_result = self.DB.db_inst.store_result()
                self.sql_insert_id = self.DB.db_inst.insert_id()
                if(re.match("^SELECT ",Query.upper())):
                        self.num_rows=self.sql_result.num_rows();
                else :  
                        self.num_rows=0
                        return True
                for i in range(0,self.num_rows):
                        row = self.sql_result.fetch_row()
                        self.result.append( row[0])
                self.DB.dbclose()
                return self.result
               
        def insert(self,table,InsertObject):
               
                whr = self.build_key_vals_from_obj(InsertObject)
                qry="INSERT INTO "+str(table)+" "+whr
                X=self.dbquery(qry)
                if(X):
                        if(self.sql_insert_id==0):
                                return "custom_id"
                        return self.sql_insert_id
                return False
        def delete(self,table,key,val):
                qry="DELETE FROM "+str(table)+" WHERE "+str(key)+"='"+str(val)+"'"
                result= self.dbquery(qry)
                if result:
                        return  self.sql_affected_ct;
                return False
        
        def select_object(self,table,selectData,delim="AND"):
                
                whr=self.build_key_eq_val_from_obj(selectData,delim);               
                return self.select_where(table,whr)
        
        def select_where(self,table,where):
                 qry="SELECT * FROM "+str(table)+" WHERE "+str(where)
                 self.dbquery(qry)
                 return self.result
          
        def select(self,table,key,value):
                return self.select_where(table,str(key)+"='"+str(value)+"'")
        def update(self,table,updateObj,where):
                qry="UPDATE %s SET %s WHERE %s"%(str(table),self.build_key_eq_val_from_obj(updateObj),str(where))
                return self.dbquery( qry )
                
        def truncate(self,table):
                qry="TRUNCATE TABLE "+table
                return self.dbquery(qry)
        def delete_where(self,table,where):
                qry="DELETE FROM "+table+" WHERE "+where
                self.dbquery(qry)
                return self.sql_affected_ct;
        def check_unique(self,table,uniqueDataObj):
                result=self.select_object(table,uniqueDataObj,"OR")
                return (self.num_rows < 1)
        def build_key_eq_val_from_obj(self,selectData,delim=","):
                whr=""
                #print selectData;
                for key in selectData:
                        val=selectData[key]
                        whr += " "+str(key)+"='"+str(val)+"' "+str(delim)
                whr= re.sub(str(delim)+"$","",whr)
                return whr
        
        def build_key_vals_from_obj(self,InsertObject):
                string0 = "("
                string1 = "Values ("
                for key in InsertObject: 
                        string0 =string0+ "`"+self.DB.dbescape(str(key))+"`,"
                        string1 =string1+ "'"+str(self.DB.dbescape(str(InsertObject[key])))+"',"
                return   re.sub(",$",")",string0)+" "+re.sub(",$",")",string1)      
class gus_database: #Gus Specific Database Interface (this is the only class we should be using)
        db=database()
        def pw_encode(self,password,salt="joran"):
                return sha1(password+salt).hexdigest()
        def associate(self,GroupID,MemberID,Role=0):
                ins= self.db.insert('associated',
                               {'key':str(GroupID)+"|"+str(MemberID),
                                'gid':GroupID,'uid':MemberID,'rid':Role})
                if(ins==False):
                        self.error_code = self.db.sql_error[0]
                        self.error_msg = self.db.sql_error[1]
                        return False
                
                return True
        def create_group(self,groupname,ownerID):
                if( not self.check_unique_groupdata({'name':groupname})):
                        self.error_code = -423
                        self.error_msg  = "Group Name Already Exists"
                        return False
                groupid =self.db.insert('gus_groups',{'owner':ownerID,'name':groupname})
                if( not groupid):
                        self.error_code = self.db.sql_error[0]
                        self.error_msg = self.db.sql_error[1]
                        return False
                return self.associate(groupid,ownerID,-10) # -10 is code for owner
                
        def del_group(self,groupID):
                self.db.delete('associated','gid',groupID) #delete all associations with group
                X= self.db.delete('gus_groups','id',groupID) #delete group
                return X
                
        def add_user(self,Username,Password,email):
                pw = self.pw_encode(Password);
                if(not self.check_email_valid(email)):
                        self.error_code =-420
                        self.error_msg = "Invalid Email Address"
                        return False
                ck = self.check_unique_userdata({'username':Username,'email':email})
                if(not ck):
                        self.error_code = -421 #arbitrary
                        self.error_msg  = "Username Or Email In Use"
                        return False ;
                ins = self.db.insert('gus_users',{'username':Username,'password':pw,'email':email})
                if(ins):
                        return ins
                self.error_code = self.db.sql_error[0]
                self.error_msg = self.db.sql_error[1]
                return False
        def del_user(self,UserID):
                #first make sure its not an owner
                if(not self.check_is_owner(UserID)):
                        self.error_code = -422
                        self.error_msg  = "Cannot Delete a Group Owner"
                        return False
               
                #remove from all groups
                self.db.delete_where('associated','uid='+str(UserID))
                 #remove from users
                return self.db.delete_where('gus_users','id='+str(UserID))
                
        def set_role(self,userID,groupID,roleID):
                r= self.db.select('associated','`key`',str(groupID)+"|"+str(userID))
                if(not len(r)): #if this isnt already in the group assoc list
                        return self.associate(groupID,userID,1) #make new assoc
                atuple = r[0] #otherwise atuple is the returned row
                if(int(atuple[3])==int(roleID)):#if its not actually changing
                        return True#return that its all good
                #else return the outcome of the update query
                return self.db.update('associated',{'rid':roleID},'`key`='+str(atuple[0]))
        def get_group_members(self,groupID):
                qry="SELECT * FROM gus_users WHERE id IN (SELECT uid FROM associated WHERE gid="+str(groupID)+")"
                return self.results_member(self.db.dbquery(qry))

        def get_members_groups(self,userID):
                qry="SELECT * FROM gus_groups WHERE id IN (SELECT gid FROM associated WHERE uid="+str(userID)+")"
                return self.results_group(self.db.dbquery(qry))


        #helpers to convert sqlresult to our Group Class
        def results_group(self,results):
                A=[]
                for i in range(0,len(results)):
                        A.append(self.result_to_group(results[i]))
                return A
        def result_to_group(self,result):
                #id=result[0]
                grp = Group(result[2],result[1])
                grp.groupID = result[0]
                return grp
        #helpers to convert sqlresult to our Member Class
        def results_member(self,results):
                A=[]
                for i in range(0,len(results)):
                        A.append(self.result_to_member(results[i]))
                return A
        def result_to_member(self,result):
           usr = Member(result[1],result[3])
           usr.userID = result[0];
           return usr
                
        #some validation helpers        
        def check_email_valid(self,email):
                return re.match("[a-zA-Z]+[a-zA-Z0-9.+-]*@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}",str(email))
        def check_is_owner(self,UserID):
                return self.check_unique_groupdata({'owner':UserID})
        def check_unique_associations(self,uniqueDataObj):
                return self.db.check_unique('associated',uniqueDataObj)
        def check_unique_groupdata(self,uniqueDataObj):
                return self.db.check_unique('gus_groups',uniqueDataObj)
        def check_unique_userdata(self,uniqueDataObj):
                return self.db.check_unique('gus_users',uniqueDataObj)
        
       


                
