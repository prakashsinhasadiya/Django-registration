# -*- coding: utf-8 -*-

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


# class ResetPasswordForm(forms.Form):
#     username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
#         attrs={'class': 'inputcustom'}))


# class ConfirmPasswordForm(forms.Form):
#     password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput(
#         attrs={'class': 'inputcustom'}))
#     password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput(
#         attrs={'class': 'inputcustom'}))
