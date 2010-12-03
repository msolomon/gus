from django import template
from django import forms
from django.template.loader import render_to_string
register = template.Library()

def userbar(user):
        return render_to_string('gus_groups/blocks/userbar.html',{'user':user,})

register.simple_tag(userbar)    

def loginform():1
	#return render_to_string('gus_groups/blocks/login.html')
def regform():1
	#return render_to_string('gus_groups/blocks/reg.html')


class role_form(forms.Form):
        users = forms.CharField(max_length=100)

def assign_group_form(role):
	rf = role_form()
	return render_to_string('gus_groups/blocks/roles.html',{'role_form':rf})
register.simple_tag(assign_group_form)    


