# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django import forms
from gus.gus_groups.models import *
from gus.gus_groups.forms import *
from django.contrib import messages
from models import *

def view_module(request,module_id,view):
	mymod = gus_module.objects.get(pk=module_id)
	from gus  import modules
	mymod_src=getattr(modules,mymod.module_name)
	vw = getattr(mymod.views,view)
	from modules import 
	
	
