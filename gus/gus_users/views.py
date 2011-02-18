from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    return HttpResponse('Something to print')

def login(request):	
    return HttpResponse('Login!')

def register(request):	
    return HttpResponse('Register!')


