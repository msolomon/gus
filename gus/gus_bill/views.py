from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from  django.template import RequestContext
from gus.gus_groups.models import *
from gus.gus_roles.models import *
from gus.gus_users.models import *
from gus.gus_bill.models import *

def index(request):
	usr = request.user
	usr = gus_user.objects.get(pk = 1)
	bills = bill.objects.filter(user = usr.id)
	#returns all the roles which the usr is an Owner
	roles = gus_role.objects.with_user(usr).filter(_role_name = "Owner")
	adbills = []
	for a in roles:
		#a.getGroup() returns the group
		#bill.objects.filter(group) returns the bills associated with that group
		#adbills will be a list of all the bills which the current user is an owner
		adbills.append(bill.objects.filter(group = a.group))

	return render_to_response('bill/index.html', {"bills":bills, "adminBills":adbills}, context_instance=RequestContext(request))
	

