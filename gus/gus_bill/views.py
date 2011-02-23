from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from  django.template import RequestContext
from gus.gus_groups.models import *
from gus.gus_roles.models import *
from gus.gus_users.models import *
from gus.gus_bill.models import *

def index(request):
	request_usr = gus_user.objects.get(pk=1)
	request_grp = gus_group.objects.get(pk=1)
	bills = bill.objects.filter(user = request_usr.id, group = request_grp)
	return render_to_response('bill/index.html', {"bills":bills}, context_instance=RequestContext(request))
	


