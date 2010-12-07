# Create your views here.
from django.shortcuts import render_to_response , redirect
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from gus.gus_talk.models import *
from django.core.urlresolvers import reverse
#from settings import MEDIA_ROOT, MEDIA_URL

def main(request,group_id = -1):
    """Main listing."""
    if (group_id == -1):
	return my_forums(request)
    user = userauthenticated(request)   
    g=gus_group()
    try:
    	grp=gus_group.objects.get(id=group_id)
    except gus_group.DoesNotExist:
	return HttpResponse("Sorry There was an internal error") 
    forums = gus_forum.objects.filter(_group=grp)
    return render_to_response("gus_talk/home.html", {'forums':forums,'user':user,'group':grp})

def my_forums(request):
    user = userauthenticated(request)   
    return render_to_response("gus_talk/myhome.html", {'forums':forums,'user':user})
	

class new_thread_form(forms.Form):
	"""autoform class for a new thread"""
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
			return HttpResponse("Critical Error Forum Not Found")
			frm=gus_forum()
		t = gus_thread(_forum=frm,_title=nmf.cleaned_data['thread_title'],creator=user._user)
		t.save()
		msg = gus_message(_body=nmf.cleaned_data['message'],_thread=t,creator=user._user,_title=t._title)
		msg.save()
    else:
        nmf=new_thread_form()
    threads = gus_thread.objects.filter(_forum=id)
    try:
			frm=gus_forum.objects.get(pk=id)
    except thrd.DoesNotExist:
			return HttpResponse("Critical Error Forum Not Found")
			frm=gus_forum()
    return render_to_response("gus_talk/forum.html", 
		{'fid':id,'threads':threads, 'user':user,'scripts':nmf.media,'forum':frm},
		context_instance=RequestContext(request) )

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
    try:
	thrd=gus_thread.objects.get(pk=id)
    except thrd.DoesNotExist:
	return HttpResponse("Critical Error Thread Does Not Exist!")
	thrd=""
    user = userauthenticated(request)
    if request.method == 'POST': # If the form has been submitted...
        nmf = new_message_form(request.POST) # A form bound to the POST data
        if nmf.is_valid(): # All validation rules pass
		msg = gus_message(_body=nmf.cleaned_data['message'],_thread=thrd,creator=user._user,_title=thrd._title)
		msg.save()
		
    else:
        nmf=new_message_form()
    grp=thrd.group()
    messages = gus_message.objects.filter(_thread=id)
    return render_to_response("gus_talk/thread.html", {'thread':gus_thread.objects.get(pk=id),'tid':id,'messages':messages, 
'user':user,'scripts':nmf.media,'group':grp},context_instance=RequestContext(request) )

