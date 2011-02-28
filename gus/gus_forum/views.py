from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from gus.gus_forum import *

def index(urlRequest):
	"""
	"""

	requesting_user = urlRequest.user
	if requesting_user.is_anonymous():
		return HttpResponseRedirect('/')
	#End

	forums = forums.objects.all()
	return render_to_response('forum/index.html', {"forums":forums}, context_instance=RequestContext(request))
#End
