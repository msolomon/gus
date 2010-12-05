from django import template
from django import forms
from django.template.loader import render_to_string
register = template.Library()
from gus.settings import MEDIA_URL

def userbar(user,group,subcontext=""):
        return render_to_string('gus_groups/blocks/userbar.html',{'user':user,'MEDIA_URL':MEDIA_URL,'content':generate_user_string(user,group)})

register.simple_tag(userbar)    

def loginform():
	return render_to_string('gus_groups/blocks/login.html')
def regform():
	return render_to_string('gus_groups/blocks/reg.html')

register.simple_tag(regform)    
register.simple_tag(loginform)    

class role_form(forms.Form):
        users = forms.CharField(max_length=100)

def assign_group_form(role):
	rf = role_form()
	return render_to_string('gus_groups/blocks/roles.html',{'role_form':rf})
register.simple_tag(assign_group_form)    


def generate_user_string(user,group,subcontext=""):
	str= "Hello "+ user.username + ", "
	str+="<a href='/logout/'>Logout</a>"
	str+="<span style='float:right;margin-right:10px'><b>["+group+subcontext+"]</b>:<a href='/profile/'>View Profile</a></span>"
	return str
