from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(urlRequest):
    return render_to_response('gallery/index.html')

def group(urlRequest, group_name):
    return render_to_response('gallery/group_listing.html', {'group_name':group_name})

def single(urlRequest, gallery_id):
    #    return render_to_response('gallery/single_gallery.html', {gallery_id})
    return ''
