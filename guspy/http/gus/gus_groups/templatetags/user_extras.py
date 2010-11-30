from django import template
from django.template.loader import render_to_string
register = template.Library()

def userbar(user):
        return render_to_string('gus_groups/userbar.html',{'user':user,})

register.simple_tag(userbar)    
