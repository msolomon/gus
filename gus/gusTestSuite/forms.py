"""
This File simply contains form definitions for our test environment
these definitions are responsible for the rendering of form elements and 
the validation of form data

they are not responsible for the data processing nor the submission of data
all forms require a cross site request forgery token provided by django
{% csrf_token %}
"""
import re
from django import forms
from gus.gus_users.models import gus_user
from gus.gus_roles.models import gus_role
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from gus.gus_groups.models import gus_group

class SimpleUserAddForm(forms.Form):
    """
    A form to add a new user to the system
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput())
    real_name=forms.CharField(max_length=150)
    email = forms.EmailField(label='Contact e-mail:')
    id  = forms.IntegerField(required=False,widget=forms.HiddenInput())
    
    def clean_username(self):
        '''
        Ensure the chosen username is unique
        '''
        data = self.cleaned_data['username'].lower()
        try:
            User.objects.get(username=data)
        except:
            data = validate_username_chars(self)
            return data
        raise forms.ValidationError('This username is already taken')
    
    
class SimpleUserEditForm(forms.Form):
    """
    A form to edit an to the system
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput())
    
    email = forms.EmailField(label='Contact e-mail:')
    id  = forms.IntegerField(required=False,widget=forms.HiddenInput())
    
    def clean_username(self):
        return validate_username_chars(self)
    
def validate_username_chars(self):
    '''
    Ensure a username only has alphanumeric and underscore characters
    '''
    uname = self.cleaned_data['username'].lower()
    cleaned = re.sub('\W', '', uname)
    if cleaned != uname:
        raise forms.ValidationError('Usernames may only contain underscores and alphanumerics')
    return uname

class SimpleAddUserToGroup(forms.Form):
    """
    A form to add a user to a group
    """
    group = forms.CharField(widget=forms.HiddenInput)
    new_member = forms.ModelChoiceField(
                            queryset=[],
                            empty_label="Select Member"
                            )
    role = forms.ModelChoiceField(queryset=[], empty_label="Select Role")
    def __init__(self, group, data=None):
        super(SimpleAddUserToGroup, self).__init__()
        self.fields[
            'new_member'
            ].queryset = gus_role.objects.users_without_group(group)
        self.fields['group'].initial = group.id
        self.fields['role'].queryset = gus_role.objects.filter(_role_group=group)
                            
class SimpleSubGroupAddForm(forms.Form):
    """
    This Form Allows the adding of new subgroups to a supergroup
    """
    group_name = forms.CharField(max_length=100)
    group_description=forms.CharField(widget=forms.Textarea,required=False)
    group_image = forms.FileField(required=False)
    parent_group=forms.IntegerField(widget=forms.HiddenInput)
                        
class SimpleGroupAddForm(forms.Form):
    """
    This is the form that allows you to add a new group
    it is responsible for both rendering and validating the form fields
    it is not responsible for the submission of the form,or the proccessing of data
    
    
    
    @return: None
    """
    group_name = forms.CharField(max_length=100)
    group_description = forms.CharField(widget=forms.Textarea, required=False)
    group_image = forms.FileField(required=False)
    group_owner = forms.ModelChoiceField(
                            queryset=gus_user.objects.all(),
                            empty_label="Select Owner"
                            )
    
    def clean_group_name(self):
        '''
        Ensure the chosen group name is unique
        '''
        data = self.cleaned_data['group_name']
        try:
            gus_group.objects.get(group_name=data)
        except:
            return data
        raise forms.ValidationError('This group name is already taken')


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
class ApprovalForm(forms.Form):
    group_id = forms.IntegerField(widget=forms.HiddenInput())
    is_active = forms.BooleanField(required=False)

class RolePermissionForm(forms.Form):
    from django.db.models import Q
    is_superUser=forms.BooleanField(required=False)
    id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    role_permissions=forms.ModelMultipleChoiceField(
                        queryset=Permission.objects.filter(name__contains="gus_")
                        )

class RoleCreateForm(forms.Form):
    role_name=forms.CharField(max_length=50)
    is_superUser=forms.BooleanField(required=False)    
    id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    role_permissions=forms.ModelMultipleChoiceField(
                        queryset=Permission.objects.filter(name__contains="gus_")
                        )
