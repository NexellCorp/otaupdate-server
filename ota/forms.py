import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from util import hex_validator


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Verify Password",
        widget=forms.PasswordInput()
    )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            p1 = self.cleaned_data['password1']
            p2 = self.cleaned_data['password2']
            if p1 == p2:
                return p2
            raise forms.ValidationError("Failed to verify password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                "Invalid username: support only alphanumeric and _")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("%s is already registered" % username)


class RomForm(forms.Form):
    device = forms.CharField(label="Device",
                             max_length=16,
                             widget=forms.TextInput(attrs={'size': 64}))
    name = forms.CharField(label="ROM Name",
                           max_length=32,
                           widget=forms.TextInput(attrs={'size': 64}))
    ota_id = forms.CharField(label="ROM OTA ID",
                             max_length=32,
                             widget=forms.TextInput(attrs={'size': 64}))
    download_url = forms.URLField(label="Download URL",
                                  widget=forms.TextInput(attrs={'size': 64}))
    md5sum = forms.CharField(label="MD5",
                             max_length=64,
                             validators=[hex_validator()],
                             widget=forms.TextInput(attrs={'size': 64}))
    version = forms.IntegerField(label="Version",
				 widget=forms.TextInput(attrs={'size': 64}))
    date = forms.DateTimeField(label="DateTime",
			       widget=forms.TextInput(attrs={'size': 64}))
    change_log = forms.CharField(label="Change Log",
                                 required=False,
                                 widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}))
