from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from  django.template import RequestContext
from gus.gus_groups.models import *
from gus.gus_roles.models import *
from gus.gus_users.models import *
from gus.gus_bill.models import *
from django import forms

class payment_bill_form(forms.Form):
  Value = forms.FloatField(min_value=0)


class new_bill_form(forms.Form):
  Name = forms.CharField(max_length = 25)
  Value = forms.IntegerField(min_value=0)
  user = forms.ModelMultipleChoiceField(queryset=gus_user.objects.all())
  def setGroup(self, group):
      role_ids =[r.id for r in group.roles]
      self.fields[
            'user'
            ].queryset = gus_role.objects.users_with_group(group)
  #      self.fields['group'].initial = group.id
  #	      self.fields['role'].queryset = gus_role.objects.filter(_role_group=group)

@login_required
def index(request):
	usr = request.user
	bills = bill.objects.filter(user = usr.id).exclude(name__contains="_archive")
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
		
		

	return render_to_response('bill/index.html', {"bills":bills, "adminGroups":adgroups, "formFint":form, "user":usr}, context_instance=RequestContext(request))
	
#AddBill
@login_required
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
      for u in form.cleaned_data['user']:
	bill_name = form.cleaned_data['Name']
	bill_val = form.cleaned_data['Value']
	bill.objects.create_bill(u, bill_grp, bill_name, bill_val)
      return HttpResponseRedirect('/bill/')
    #no form data recieved
  form = new_bill_form()    
  form.setGroup(bill_grp)
  return render_to_response('bill/add_bill.html',{'group':bill_grp,'form':form},
			    context_instance=RequestContext(request))

#Delete
@login_required
def DeleteBill(request,bill_id=-1):
  try:
    b = bill.objects.get(pk=bill_id)
  except:
    return HttpResponse('Bill Not Found')
  b.delete()
  return HttpResponseRedirect('/bill/')

#PAYMENTS
#class payment_bill_form(forms.Form):
#  Value = forms.FloatField(min_value=0)

@login_required
def Payments(request, bill_id=-1):
  try:
    b = bill.objects.get(pk=bill_id)
  except:
    return HttpResponse('Bill Not Found')
  paymnts = payment.objects.filter(mybill = b)
  if request.method == "POST":
    form = payment_bill_form(request.POST)
    if form.is_valid():
      bill_payment = form.cleaned_data['Value']
      b.make_payment(bill_payment)
      pass
  else:
    form = payment_bill_form()
  balance = b.value - b.paid_balance()
  return render_to_response('bill/payments.html',{'payments':paymnts,'form':form, 'bill':b, 'balance':balance},
			    context_instance=RequestContext(request))

@login_required
def Archive(request, bill_id=-1):
  try:
    b = bill.objects.get(pk=bill_id)
  except:
    return HttpResponse('Bill Not Found')
  b.archive()
  return HttpResponseRedirect('/bill/')
  
  