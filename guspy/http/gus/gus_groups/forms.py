from django import forms
class reg_form(forms.Form):
        real_name=forms.CharField(max_length=50)
        email=forms.EmailField()
        username=forms.CharField(max_length=50)
        password=forms.CharField(widget=forms.PasswordInput , max_length=50,min_length=6)
class login_form(forms.Form):
        username=forms.CharField(max_length=50)
        password=forms.CharField(widget=forms.PasswordInput , max_length=50,min_length=6)


