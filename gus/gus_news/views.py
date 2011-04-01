from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from gus_news.models import *
from gus_users.models import gus_user
from django import forms

def upload_form(request):
    form = News_form()
    return render_to_response("news/upload.html",
                            {   'news_form':form, },
                                #'headline': headline, 
                                #'date': date, 
                                #'shortdesc': shortdesc, 
                                #'content': content}, 
                                context_instance=RequestContext(request))
