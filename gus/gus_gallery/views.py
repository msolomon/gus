# GUS Gallery Views
# Part of the GusPy Project
# Stephen Fischer

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.template import RequestContext
from gus_gallery.models import *
from gus_groups.models import gus_group
from gus_groups.utils import *
from gus_roles.models import *

@login_required
def gallery_add(urlRequest, group_id):
    """
    The view for adding a new gallery
    """
    the_user = urlRequest.user
    try:
        the_group = gus_group.objects.get(pk = group_id)
    except:
        return HttpResponseRedirect('/gallery/')
    error = False

    # If the user doesn't have permission to add a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can add gus_gallery"):
        return HttpResponseRedirect('/gallery/')

    if urlRequest.method == "POST":
        # If the user just posted data to the form, and it validates, add it
        the_form = gallery_form(urlRequest.POST)
        if the_form.is_valid():
            new_gallery = the_form.save(commit=False)
            new_gallery.group = gus_group.objects.filter(pk=group_id)[0]
            new_gallery.user = the_user
            new_gallery.save()
            return HttpResponseRedirect('/gallery/')
        else:
            error = True
            
    # Otherwise, present them with the gallery form
    the_form = gallery_form()
    return render_to_response('gallery/gallery_add.html',
                              {'gallery_form' : the_form,
                               'error' : error},
                              context_instance=RequestContext(urlRequest))

@login_required
def gallery_delete(urlRequest, gallery_id):
    """
    The view for deleting a gallery
    """
    the_user = urlRequest.user
    
    # If the gallery isn't valid, return to the list of galleries
    try:
        gallery = gus_gallery.objects.filter(pk=gallery_id)[0]
    except:
        return HttpResponseRedirect('/gallery')

    the_group = gallery.group

    # If the user doesn't have permission to delete a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can delete gus_gallery"):
        return HttpResponseRedirect('/gallery/')

    # If the form was posted back to the page, the user wants to delete the gallery
    if urlRequest.method == "POST":
        gallery.delete()
        return HttpResponseRedirect('/gallery')

    # Otherwise, show the user the deletion confirmation screen
    return render_to_response('gallery/gallery_delete.html',
                              {'gallery' : gallery},
                              context_instance=RequestContext(urlRequest))

@login_required
def gallery_edit(urlRequest, gallery_id):
    """
    The view for editing a gallery
    """
    the_user = urlRequest.user
    error = False

    # If the gallery isn't valid, return the user to the gallery list
    try:
        gallery = gus_gallery.objects.filter(pk = gallery_id)[0]
    except:
        return HttpResponseRedirect('/gallery')

    the_group = gallery.group

    # If the user doesn't have permission to add a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can change gus_gallery"):
        return HttpResponseRedirect('/gallery/')#region Methods

    if urlRequest.method == "POST":
        # If the user just posted data to the form, and it validates, update it
        the_form = gallery_form(urlRequest.POST, instance=gallery)
        if the_form.is_valid():
            the_form.save()
            return HttpResponseRedirect('/gallery/')   
        else:
            error = True

    # If the form isn't posted to us, or it doesn't validate, then we get the
    # form, fill it with initial data, and push it to the user
    form = gallery_form(model_to_dict(gallery))
    return render_to_response('gallery/gallery_edit.html',
                              {'gallery' : gallery,
                               'gallery_form' : form, 
                               'error' : error},
                              context_instance=RequestContext(urlRequest))

def gallery_group_list(urlRequest, group_id):
    """
    A view for a single group's galleries
    """
    the_user = urlRequest.user

    # If the group isn't legit, then redirect to the list of galleries
    try:
        the_group = gus_group.objects.filter(pk = group_id)[0]
    except:
        return HttpResponseReditect('/gallery/')

    # If the user isn't in the group, then redirect to the public gallery view
    if gus_role.objects.with_user_in_group(the_group, the_user) == None:
        return HttpResponseRedirect('/gallery/public/group/' + str(group_id))

    # Get the list of group galleries
    galleries = gus_gallery.objects.filter(group = the_group)

    # Get the user's permissions for these galleries
    can_add = False
    can_edit = False
    can_delete = False

    if the_user.has_group_perm(the_group, "Can add gus_gallery"):
        can_add = True
    if the_user.has_group_perm(the_group, "Can change gus_gallery"):
        can_edit = True
    if the_user.has_group_perm(the_group, "Can delete gus_gallery"):
        can_delete = True

    return render_to_response('gallery/gallery_group_list.html',
                              {'the_group' : the_group,
                               'galleries' : galleries,
                               'can_add' : can_add,
                               'can_edit' : can_edit,
                               'can_delete' : can_delete},
                              context_instance = RequestContext(urlRequest))

def gallery_view(urlRequest, gallery_id):
    """
    A view for a single gallery
    """
    show_gallery = False
    can_add = False
    can_delete = False
    can_edit = False

    # If the gallery isn't legit, redirect to the list of galleries
    try:
        the_gallery = gus_gallery.objects.filter(pk = gallery_id)[0]
    except:
        return HttpResponseRedirect('/gallery/')

    the_user = urlRequest.user
    the_group = the_gallery.group

    if not the_user.is_authenticated() and the_gallery.is_public:
        # If the user isn't logged in and the gallery is public, show it
        show_gallery = True
    if the_user.is_authenticated():
        if gus_role.objects.with_user_in_group(the_group, the_user):
            # If the user is a member of the group, get their perms
            can_add = the_user.has_group_perm(the_group, "Can add gus_image")
            can_delete = the_user.has_group_perm(the_group, "Can delete gus_image")
            can_edit = the_user.has_group_perm(the_group, "Can change gus_image")
            show_gallery = True
        if the_gallery.is_public:
            # If the gallery is public, show the gallery
            show_gallery = True

    # If we want to show the gallery, do it. Otherwise, redirect the user
    if show_gallery:
        the_images = the_gallery.get_images()
        return render_to_response('gallery/gallery_view.html',
                                  {'gallery' : the_gallery,
                                   'images' : the_images,
                                   'can_add' : can_add,
                                   'can_delete' : can_delete,
                                   'can_edit' : can_edit},
                                  context_instance = RequestContext(urlRequest))
    return HttpResponseRedirect('/gallery/')


@login_required
def image_add(urlRequest, gallery_id):
    """
    A view for adding an image to a gallery
    """
    the_user = urlRequest.user
    error = False

    # Make sure it's a valid gallery, if not, redirect the user to the gallery page
    try:
        gallery = gus_gallery.objects.filter(pk=gallery_id)[0]
    except:
        return HttpResponseRedirect('/gallery')

    the_group = gallery.group

    # If the user doesn't have permission to add a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can add gus_image"):
        return HttpResponseRedirect('/gallery/')

    if urlRequest.method == "POST":
        # If the user just posted data to the form, and it validates, update it
        form = image_form(urlRequest.POST, urlRequest.FILES)
        if form.is_valid():
            # Save the image, take the user back to the gallery
            new_image = form.save(commit=False)
            new_image.gallery = gallery
            new_image.user = the_user
            new_image.save()
            return HttpResponseRedirect('/gallery/' + gallery_id)
        else:
            error = True

    # If the form wasn't just posted to us, or it wasn't valid, then show the page to
    # add a new image
    form = image_form()
    return render_to_response('gallery/image_add.html',
                              {'gallery' : gallery,
                               'image_form' : form,
                               'error' : error},
                              context_instance = RequestContext(urlRequest))

@login_required
def image_delete(urlRequest, image_id):
    """
    A view for deleting an image from a gallery
    """
    the_user = urlRequest.user
    error = False

    # If the image isn't legit, return to the gallery list
    try:
        image = gus_image.objects.filter(pk = image_id)[0]
    except:
        return HttpResponseRedirect('/gallery')

    gallery = image.gallery
    the_group = gallery.group

    # If the user doesn't have permission to add a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can delete gus_image"):
        return HttpResponseRedirect('/gallery/')

    # If the form has been posted, the user wants to delete the image. So do it
    if urlRequest.method == "POST":
        image.delete()
        return HttpResponseRedirect('/gallery/' + str(gallery.id))

    # Otherwise, show the normal view
    return render_to_response('gallery/image_delete.html',
                              {'gallery' : gallery,
                               'image' : image,
                               'error' : error},
                              context_instance = RequestContext(urlRequest))

@login_required
def image_edit(urlRequest, image_id):
    """
    The view for editing an existing image in a gallery
    """
    the_user = urlRequest.user
    error = False

    # If the image isn't legit, return to the gallery listing
    try:
        image = gus_image.objects.filter(pk = image_id)[0]
    except:
        return HttpResponseRedirect('/gallery')

    gallery = image.gallery
    the_group = gallery.group

    # If the user doesn't have permission to add a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can change gus_image"):
        return HttpResponseRedirect('/gallery/')

    # If the form has been posted, handle it
    if urlRequest.method == "POST":
        # If the user just posted data to the form, and it validates, update it
        the_form = image_edit_form(urlRequest.POST, instance=image)
        if the_form.is_valid():
            the_form.save()
            return HttpResponseRedirect('/gallery/' + str(gallery.id))
        else:
            error = True

    # Otherwise, if the form hasn't been posted, fill it with information
    form = image_edit_form(model_to_dict(image))    
    return render_to_response('gallery/image_edit.html',
                              {'gallery' : gallery,
                               'image' : image,
                               'image_form' : form,
                               'error' : error},
                              context_instance = RequestContext(urlRequest))

@login_required
def index(urlRequest):
    """
    The default view that shows all galleries for all groups
    """
    the_user = urlRequest.user

    # Get all the groups that the user belongs to, if any, and all the
    # galleries for those groups
    groups = getGroupsWithUser(the_user)    

    galleries = []
    for g in groups:
        for gal in gus_gallery.objects.filter(group=g):
            galleries.append(gal)

    # Get the list of groups that the user can add/edit/delete galleries for
    can_add = []
    can_edit = []
    can_delete = []
    for g in groups:
        if the_user.has_group_perm(g, "Can add gus_gallery"):
            can_add.append(g)
        if the_user.has_group_perm(g, "Can change gus_gallery"):
            can_edit.append(g)
        if the_user.has_group_perm(g, "Can delete gus_gallery"):
            can_delete.append(g)

    return render_to_response('gallery/index.html',
                              {'groups' : groups,
                               'galleries' : galleries,
                               'can_add' : can_add,
                               'can_edit' : can_edit,
                               'can_delete' : can_delete},
                              context_instance = RequestContext(urlRequest))

def public_group(urlRequest, group_id):
    """
    The view for a list of public galleries for a given group
    """
    # See if the group is valid, if not return to a list of all public galleries
    try:
        the_group = gus_group.objects.filter(pk = group_id)[0]
    except:
        return HttpResponseRedirect('/gallery/public')

    # Get the public galleries for a given group
    group_galleries = gus_gallery.objects.filter(group = the_group)
    galleries = []

    for g in gus_gallery.objects.filter(group = the_group):
        if g.is_public:
            galleries.append(g)

    # Return the user to the list of public group galleries
    return render_to_response('gallery/gallery_group_public_list.html',
                              {'the_group' : the_group,
                               'galleries' : galleries,
                               'can_add' : False,
                               'can_edit' : False,
                               'can_delete' : False},
                              context_instance = RequestContext(urlRequest))    

def public_list(urlRequest):
    """
    The view for a list of all public image galleries
    """
    # Get the public galleries
    galleries = gus_gallery.objects.filter(is_public = True)
    if len(galleries) == 0:
        galleries = None

    return render_to_response('gallery/public_list.html',
                              {'galleries' : galleries},
                              context_instance = RequestContext(urlRequest))
