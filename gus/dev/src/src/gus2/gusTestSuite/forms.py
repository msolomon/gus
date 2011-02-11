"""
This File simply contains forms for our test environment
"""

from django import forms
from gus2.gus_users.models import gus_user
from gus2.gus_roles.models import gus_role

class SimpleUserAddForm(forms.Form):
    """
    A form to add a new user to the system
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    email = forms.EmailField()

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
                            
                    
class SimpleGroupAddForm(forms.Form):
    """
    dhgdhgdhdh
    jfhfhfghf
    
    
    @return: this return blah
    """
    group_name = forms.CharField(max_length=100)
    group_description = forms.CharField(widget=forms.Textarea, required=False)
    group_image = forms.FileField(required=False)
    group_owner = forms.ModelChoiceField(
                            queryset=gus_user.objects,
                            empty_label="Select Owner"
                            )


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

