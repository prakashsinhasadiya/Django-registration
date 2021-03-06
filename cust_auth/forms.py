# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput())
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())


class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput())
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput())
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = forms.CharField(validators=[phone_regex],max_length=17, required=True,
                             widget=forms.TextInput())
    email = forms.EmailField(
        required=True, widget=forms.EmailInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            message = "User alresy existes with this email"
            raise ValidationError(message)
        return email
    def clean_password2(self):
        import pdb; pdb.set_trace()
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
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = forms.CharField(validators=[phone_regex],max_length=17, required=True,
                             widget=forms.TextInput())
    # def clean_mobile(request):
    #     import pdb; pdb.set_trace()
    #     mobile = self.cleaned_data.get('mobile')

class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput())



class ConfirmPasswordForm(forms.Form):
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    
    def clean_password(self):
        import pdb; pdb.set_trace()
        password_2 = self.cleaned_data.get('password_2')
        password_1 = self.cleaned_data.get('password_1')
        if password_1 and password_2 and password_1 != password_2:
            message = "Passwords do` not match"
            raise ValidationError(message)
        return password_2