from django import forms
from django.contrib.auth.models import User
from .models import Profile

''' we here inherit from ModelForm not Form because 
    we are working with model '''


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfieEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)
        ''' to control form to prevent currently image url from appearing
        in edit form (look at edit.html also)'''
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = {"username", "email", "last_name"}

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError("passwords do not match")
        return self.cleaned_data['password2']
