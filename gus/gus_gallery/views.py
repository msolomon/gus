from django.http import HttpResponse
from django.shortcuts import render_to_response
from gus2.gus_groups.models import *

def index(urlRequest):
    return render_to_response('gallery/index.html')

def group(urlRequest, slug):
    g = gus_group.objects.filter(group_slug=slug)

    if(len(g) == 0):
        raise Exception('Group does not exist!')

    return render_to_response('gallery/group_listing.html', {'group':g[0]})

def single(urlRequest, gallery_id):
    #    return render_to_response('gallery/single_gallery.html', {gallery_id})
    return ''
