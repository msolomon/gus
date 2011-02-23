from django.shortcuts import render_to_response
from django.http import HttpResponse
from  django.template import RequestContext

from gus_emailer.models import EmailerWidget

def index(request):
	return render_to_response('email/index.html', {'listing' : dir(EmailerWidget)}, context_instance=RequestContext(request))
