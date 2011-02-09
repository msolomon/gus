from django.http import HttpResponse

def index(urlRequest):
    return HttpResponse('hello')

