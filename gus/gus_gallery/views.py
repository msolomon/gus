# TODO: Handle attempting to add an invalid image gallery better? Right now it just fails silently, and stays at the form
# TODO: Add permission stuff in here so not everyone can perform these actions (only needed in index now)
# TODO: Add the ability for galleries to be flagged public
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.template import RequestContext
from gus.gus_gallery.models import *
from gus.gus_groups.models import *
from gus.gus_groups.utils import *

@login_required
def gallery_add(urlRequest, group_id):
    """
    The view for adding a new gallery
    """
    the_user = urlRequest.user
    the_group = gus_group.object.filter(pk = group_id)

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

    # Otherwise, present them with the gallery form
    the_form = gallery_form()
    return render_to_response('gallery/gallery_add.html',
                              {'gallery_form' : the_form},
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

    # If the form isn't posted to us, or it doesn't validate, then we get the
    # form, fill it with initial data, and push it to the user
    form = gallery_form(model_to_dict(gallery))
    return render_to_response('gallery/gallery_edit.html',
                              {'gallery' : gallery, 'gallery_form' : form},
                              context_instance=RequestContext(urlRequest))

@login_required
def gallery_view(urlRequest, gallery_id):
    """
    A view for a single gallery
    """
    gallery = gus_gallery.objects.filter(pk=gallery_id)[0]
    images = gallery.get_images()

    # If the user isn't in the group, redirect to the list of galleries
    the_user = urlRequest.user
    if gus_role.objects.with_user_in_group(gallery.group, the_user) == None:
        return HttpResponseRedirect('/gallery/')

    # Get the permissions for the current gallery
    the_group = gallery.group;
    can_add = the_user.has_group_perm(the_group, "Can add gus_image")
    can_edit = the_user.has_group_perm(the_group, "Can edit gus_image")
    can_delete = the_user.has_group_perm(the_group, "Can delete gus_image")

    return render_to_response('gallery/gallery_view.html',
                              {'gallery' : gallery,
                               'images' : images,
                               'can_add' : can_add,
                               'can_edit' : can_edit,
                               'can_delete' : can_delete})

@login_required
def image_add(urlRequest, gallery_id):
    """
    A view for adding an image to a gallery
    """
    the_user = urlRequest.user

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

    # If the form wasn't just posted to us, or it wasn't valid, then show the page to
    # add a new image
    form = image_form()
    return render_to_response('gallery/image_add.html',
                              {'gallery' : gallery, 'image_form' : form},
                              context_instance = RequestContext(urlRequest))

@login_required
def image_delete(urlRequest, image_id):
    """
    A view for deleting an image from a gallery
    """
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
        return HttpResponseRedirect('/gallery/' + `gallery.id`)

    # Otherwise, show the normal view
    return render_to_response('gallery/image_delete.html',
                              {'gallery' : gallery, 'image' : image},
                              context_instance = RequestContext(urlRequest))

@login_required
def image_edit(urlRequest, image_id):
    """
    The view for editing an existing image in a gallery
    """
    # If the image isn't legit, return to the gallery listing
    try:
        image = gus_image.objects.filter(pk = image_id)[0]
    except:
        return HttpResponseRedirect('/gallery')

    gallery = image.gallery
    the_group = gallery.group
    the_user = urlRequest.user

    # If the user doesn't have permission to add a gallery, redirect them
    if not the_user.has_group_perm(the_group, "Can add gus_image"):
        return HttpResponseRedirect('/gallery/')

    # If the form has been posted, handle it
    if urlRequest.method == "POST":
        # If the user just posted data to the form, and it validates, update it
        the_form = image_edit_form(urlRequest.POST, instance=image)
        if the_form.is_valid():
            the_form.save(commit=False)
            return HttpResponseRedirect('/gallery/' + `gallery.id`)

    # Otherwise, if the form hasn't been posted, fill it with information
    form = image_edit_form(model_to_dict(image))    
    return render_to_response('gallery/image_edit.html',
                              {'gallery' : gallery,
                               'image' : image,
                               'image_form' : form},
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

    return render_to_response('gallery/index.html',
                              {'groups' : groups, 'galleries' : galleries},
                              context_instance=RequestContext(urlRequest))
