# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'inputcustom'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'inputcustom'}))


class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'inputcustom'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'inputcustom'}))
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'inputcustom'}))
    password_1 = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'inputcustom'}))
    password_2 = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'inputcustom'}))
    mobile = forms.CharField(max_length=10, required=True,
                             widget=forms.TextInput(attrs={'class': 'inputcustom'}))
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': 'inputcustom'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            message = "User alresy existes with this email"
            raise ValidationError(message)
        return email
    def clean_password2(self):
        password_2 = self.cleaned_data.get('password_2')
        password_1 = self.cleaned_data.get('password_1')
        if password_1 and password_2 and password_1 != password_2:
            message = "Passwords do not match"
            raise ValidationError(message)
        return password_2
# class ResetPasswordForm(forms.Form):
#     username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
#         attrs={'class': 'inputcustom'}))


# class ConfirmPasswordForm(forms.Form):
#     password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput(
#         attrs={'class': 'inputcustom'}))
#     password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput(
#         attrs={'class': 'inputcustom'}))

class ProfileForm(forms.Form):

    mobile = forms.CharField(max_length=10, required=True,
                             widget=forms.TextInput(attrs={'class': 'inputcustom'}))

    # def clean_mobile(request):
    #     import pdb; pdb.set_trace()
    #     mobile = self.cleaned_data.get('mobile')

class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'input100'}))



class ConfirmPasswordForm(forms.Form):
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'input100'}))
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'input100'}))
