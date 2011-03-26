from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from gus.gus_gallery.models import *
from gus.gus_groups.utils import *

def add(urlRequest):
    """
    The view for adding a new gallery
    """
    # If the user isn't validated, take them to the GUS homepage
    the_user = urlRequest.user
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    # Otherwise, present them with the gallery form
    the_form = gallery_form()
    return render_to_response('gallery/add_form.html',
                              {the_form : "gallery_form"},
                              context_instance=RequestContext(urlRequest))


def delete(urlRequest, gallery_id):
    """
    The view for deleting a gallery
    """
    # If the user isn't validated, take them to the GUS homepage
    the_user = urlRequest.user
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    return render_to_response('gallery/delete.html',
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

    return render_to_response('gallery/edit_form.html',
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
        galleries.append(gus_gallery.objects.filter(group=g))

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

    return render_to_response('gallery/single_gallery.html',
                              {'gallery' : gallery_id})
