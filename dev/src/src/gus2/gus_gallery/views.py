from django.http import HttpResponse

def index(urlREQUEST):
    return HttpResponse('hello')

