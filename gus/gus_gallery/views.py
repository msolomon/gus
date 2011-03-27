# TODO: Handle attempting to add an invalid image gallery better? Right now it just fails silently, and stays at the form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from gus.gus_gallery.models import *
from gus.gus_groups.models import *
from gus.gus_groups.utils import *

def add(urlRequest):
    """
    The view for adding a new gallery
    """
    # If the user isn't validated, take them to the GUS homepage
    the_user = urlRequest.user
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    if urlRequest.method == "POST":
        # If the user just posted data to the form, and it validates, add it
        the_form = gallery_form(urlRequest.POST)
        if the_form.is_valid():
            new_gallery = the_form.save(commit=False)
            new_gallery.group = gus_group.objects.filter(pk=1)[0]
            new_gallery.user = the_user
            new_gallery.save()
            
            return HttpResponseRedirect('/gallery/')

    # Otherwise, present them with the gallery form
    the_form = gallery_form()
    return render_to_response('gallery/gallery_add.html',
                              {'gallery_form' : the_form},
                              context_instance=RequestContext(urlRequest))


def delete(urlRequest, gallery_id):
    """
    The view for deleting a gallery
    """
    # If the user isn't validated, take them to the GUS homepage
    the_user = urlRequest.user
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    return render_to_response('gallery/gallery_delete.html',
                              {},
                              context_instance=RequestContext(urlRequest))


def edit(urlRequest, gallery_id):
    """
    The view for editing a gallery
    """
    # If the user isn't validated, take them to the GUS homepage
    the_user = urlRequest.user
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    return render_to_response('gallery/gallery_edit.html',
                              {},
                              context_instance=RequestContext(urlRequest))


def index(urlRequest):
    """
    The default view that shows all galleries for all groups
    """
    the_user = urlRequest.user

    # If the user isn't validated, take them to the GUS homepage
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    # Get all the groups that the user belongs to, if any, and all the
    # galleries for those groups
    groups = getGroupsWithUser(the_user)    

    galleries = []
    for g in groups:
        for gal in gus_gallery.objects.filter(group=g):
            galleries.append(gal)

    return render_to_response('gallery/index.html',
                              {'groups' : groups, 'galleries' : galleries},
                              context_instance=RequestContext(urlRequest))


def single(urlRequest, gallery_id):
    """
    A view for a single gallery
    """
    # If the user isn't validated, take them to the GUS homepage
    the_user = urlRequest.user
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    the_gallery = gus_gallery.objects.filter(pk=gallery_id)[0]
    return render_to_response('gallery/gallery_view.html',
                              {'gallery' : the_gallery})
