from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
	return HttpResponse('Welcome to the land of views')
