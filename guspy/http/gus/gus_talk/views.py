# Create your views here.
from django.shortcuts import render_to_response , redirect
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from gus.gus_talk.models import *
from django.core.urlresolvers import reverse
#from settings import MEDIA_ROOT, MEDIA_URL

def main(request):
    """Main listing."""
    user = userauthenticated(request)   
    forums = gus_forum.objects.all()
    return render_to_response("gus_talk/home.html", dict(forums=forums,
							 user=user))


class new_thread_form(forms.Form):
	message	  = forms.CharField(widget=forms.Textarea,max_length=10000)
	thread_title = forms.CharField(max_length=50)
	fid = forms.IntegerField();
		
	class Media:
		css={'all':('css/gus_forums.css',)}
		js=('js/jquery.js',)

def forum(request,id):
    """Main listing."""
    user = userauthenticated(request)
    if not user : return redirect('/login/')
    if request.method == 'POST': # If the form has been submitted...
        nmf = new_thread_form(request.POST) # A form bound to the POST data
        if nmf.is_valid(): # All validation rules pass
		try:
			frm=gus_forum.objects.get(pk=id)
		except thrd.DoesNotExist:
			frm=gus_forum()
		t = gus_thread(_forum=frm,_title=nmf.cleaned_data['thread_title'],creator=user._user)
		t.save()
		msg = gus_message(_body=nmf.cleaned_data['message'],_thread=t,creator=user._user,_title=t._title)
		msg.save()
    else:
        nmf=new_thread_form()
    threads = gus_thread.objects.filter(_forum=id)
    return render_to_response("gus_talk/forum.html", {'fid':id,'threads':threads, 'user':user,'scripts':nmf.media},context_instance=RequestContext(request) )

class new_message_form(forms.Form):
	message	  = forms.CharField(widget=forms.Textarea,max_length=10000)
	tid = forms.IntegerField();
	class Meta:
		fields=['message',]
	class Media:
		css={'all':('css/gus_forums.css',)}
		js=('js/jquery.js',)

def thread(request,id):
    """Main listing."""
    user = userauthenticated(request)
    if request.method == 'POST': # If the form has been submitted...
        nmf = new_message_form(request.POST) # A form bound to the POST data
        if nmf.is_valid(): # All validation rules pass
		try:
			thrd=gus_thread.objects.get(pk=id)
		except thrd.DoesNotExist:
			thrd=""
		msg = gus_message(_body=nmf.cleaned_data['message'],_thread=thrd,creator=user._user,_title=thrd._title)
		msg.save()
		
    else:
        nmf=new_message_form()

    messages = gus_message.objects.filter(_thread=id)
    return render_to_response("gus_talk/thread.html", {'thread':gus_thread.objects.get(pk=id),'tid':id,'messages':messages, 'user':user,'scripts':nmf.media},context_instance=RequestContext(request) )

