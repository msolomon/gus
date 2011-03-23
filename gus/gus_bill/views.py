from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from  django.template import RequestContext
from gus.gus_groups.models import *
from gus.gus_roles.models import *
from gus.gus_users.models import *
from gus.gus_bill.models import *
from django import forms

class new_bill_form(forms.Form):
  Name = forms.CharField(max_length = 25)
  Value = forms.IntegerField(min_value=0)
  user = forms.ModelChoiceField(queryset=gus_user.objects.all(), empty_label="Select User")
  #def __init__(self, data=None):
  #      super(SimpleAddUserToGroup, self).__init__()
  #      self.fields[
  #          'new_member'a
  #          ].queryset = gus_role.objects.users_without_group(group)
  #      self.fields['group'].initial = group.id
  #	      self.fields['role'].queryset = gus_role.objects.filter(_role_group=group)

def index(request):
	if not request.user.is_authenticated():
	   return HttpResponseRedirect('/login/')
	usr = request.user
	usr = gus_user.objects.get(pk = 1)
	bills = bill.objects.filter(user = usr.id)
	#returns all the roles which the usr is an Owner
	
	form = new_bill_form()
	
	roles = gus_role.objects.with_user(usr).filter(_role_name = "Owner")
	adgroups = []
	adbills = []
	adbillsbygroup = []
	for a in roles:
		#a.getGroup() returns the group
		#bill.objects.filter(group) returns the bills associated with that group
		#adbills will be a list of all the bills which the current user is an owner
		AGRP = a.group
		AGRP.my_bills  = bill.objects.filter(group = a.group)
		adgroups.append(AGRP)
		
		

	return render_to_response('bill/index.html', {"bills":bills, "adminGroups":adgroups, "formFint":form}, context_instance=RequestContext(request))
	
def AddBill(request,group_id=-1):
  try:
	bill_grp = gus_group.objects.get(pk=group_id)
  except:
	return HttpResponseRedirect('/bill/')	
  mygrprole = gus_role.objects.with_user_in_group(bill_grp,request.user)
  if(not mygrprole or mygrprole._role_permission_level < 1):
      return HttpResponseRedirect('/bill/')	
  if request.method == "POST":
    form = new_bill_form(request.POST)
    if form.is_valid() :
      bill_name = form.cleaned_data['Name']
      bill_val = form.cleaned_data['Value']
      bill_rcpt = form.cleaned_data['user']
      bill.objects.create_bill(bill_rcpt, bill_grp, bill_name, bill_val)
      pass
  else:
    #no form data recieved
    form = new_bill_form()
    
  return render_to_response('bill/add_bill.html',{"group":bill_grp,'form':form},
			    context_instance=RequestContext(request))
  return HttpResponse("Adding a bill to group %s"%group_id)
