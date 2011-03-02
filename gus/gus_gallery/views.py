from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from gus.gus_gallery.utils import *
from gus.gus_groups.models import *
from gus.gus_roles.models import *
from gus.gus_users.models import *


def index(urlRequest):
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

    return render_to_response('gallery/index.html', {'groups': groups})


def group(urlRequest, slug):
    g = gus_group.objects.filter(group_slug=slug)

    if(len(g) == 0):
        raise Exception('Group does not exist!')

    return render_to_response('gallery/group_listing.html', {'group': g[0]})


def single(urlRequest, gallery_id):
    return render_to_response('gallery/single_gallery.html', {'gallery': gallery_id})
