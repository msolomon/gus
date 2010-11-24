# Create your views here.
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from gus.gus_talk.models import *
from django.core.urlresolvers import reverse
#from settings import MEDIA_ROOT, MEDIA_URL

def main(request):
    """Main listing."""
    forums = gus_forum.objects.all()
    return render_to_response("gus_talk/home.html", dict(forums=forums, user=request.user))

def forum(request,id):
    """Main listing."""
    threads = gus_thread.objects.filter(_forum=id)
    return render_to_response("gus_talk/forum.html", dict(threads=threads, user=request.user) )

def thread(request,id):
    """Main listing."""
    print "Thread "+str(id)
    messages = gus_message.objects.filter(_thread=id)
    print(messages)
    return render_to_response("gus_talk/thread.html", dict(messages=messages, user=request.user) )
