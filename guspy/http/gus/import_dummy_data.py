# from collections import deque
from gus_groups.models import *

def put_together_1st_quoted(sstr):
	if not len(sstr): return None
	gn=sstr[0][1:]
	sstr.pop(0)
	if gn[len(gn)-1]=="\"":
		gn = gn[:-1]
	else :
		gn2=sstr[0]
		while gn2[len(gn2)-1]!="\"":
			gn=gn+" "+gn2
			sstr.pop(0)
			gn2 = sstr[0]
			
		gn2 = gn2[:-1]
		sstr.pop(0)
		gn=gn+" "+gn2
	return gn
def proc_members(ulist,roles):
	for user in ulist:
		print "Find "+user[1:]
		user = get_user_by_fullname(user[1:])
		print user	
def gparse(str):
	sstr = str.split()
	strs=[]
	str =put_together_1st_quoted(sstr)
	strs.append(str)
	while(str):		
		str = put_together_1st_quoted(sstr)
		if str : strs.append(str)
	gn = strs.pop(0)
	grp=gus_group(group_name=gn)
	grp.save()
	roles={
		'O':gus_roles.objects.get(gid=grp,role_name="Owner"),
		'A':gus_roles.objects.get(gid=grp,role_name="Admin"),
		'M':gus_roles.objects.get(gid=grp,role_name="Member"),
	}
	proc_members(strs,roles)
	# print "GROUP[ "	+gn+" ]"
	return str;
def uparse(str):
	# print "Parse : "+str
	sstr = str.split()
	print sstr
	fn = sstr[0][1:]
	ln = sstr[1][:-1]
	un = sstr[2][1:-1]
	em = sstr[3][1:-1]
	pw = sstr[4][1:-1]
	usr = gus_user()
	usr.username = un
	usr.email=em
	usr.set_password(pw)
	usr.save()
	print usr.username 
	print "USER[("+un+") "+fn+" "+ln+"<"+em+">]"	
	return str;
	
def importfile(fname):
	try:
		fh=open(fname,"r")
	except IOError:
		return "error file not found"
	ctx=None
	lines=fh.readlines()
	for line in lines:
		if line =="\n" : continue
		if line.find('Users')==0:
			ctx=uparse
		elif line.find('Groups')==0:
			ctx=gparse
		else:
			ll=ctx(line)
	
	return lines
	
print importfile("../VIEWS/dummy_data/setup.dat")
