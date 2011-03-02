# TODO: Remove the debugging code in this before it goes live
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from gus.gus_groups.models import *
from gus.gus_roles.models import *
from gus.gus_users.models import *


def add(urlRequest):
    """
    The view for adding a new gallery
    """
    the_form = gallery_form();
    return render_to_response('gallery/add_form.html', {the_form:"gallery_form"} )


def delete(urlRequest, gallery_id):
    """
    The view for deleting a gallery
    """
    return render_to_response('gallery/delete.html')


def edit(urlRequest, gallery_id):
    """
    The view for editing a gallery
    """
    return render_to_response('gallery/edit_form.html')


def index(urlRequest):
    """
    The default view that shows all galleries for all groups
    """
    # DEBUG: These lines are for testing only
    groups = map(lambda x: x.group, gus_role.objects.with_user(1))
    if(len(groups) == 0):
        groups = None
    return render_to_response('gallery/index.html', {'groups': groups})
    # END DEBUG

    the_user = urlRequest.user

    # If the user isn't validated, take them to the GUS homepage
    if the_user.is_anonymous():
        return HttpResponseRedirect('/')

    # Get all the groups that the user belongs to, if any
    groups = map(lambda x: x.group, gus_role.objects.with_user(the_user))
    if(len(groups) == 0):
        groups = None

    # Get all the galleries for those groups
    for g in groups:
        galleries += gus_gallery.objects.filter(group=g)

    return render_to_response('gallery/index.html', {'groups': groups})


def single(urlRequest, gallery_id):
    """
    A view for a single gallery
    """
    return render_to_response('gallery/single_gallery.html', {'gallery': gallery_id})
