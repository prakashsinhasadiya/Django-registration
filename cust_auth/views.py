# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.http import Http404
from .forms import LoginForm, SignupForm,ProfileForm,ResetPasswordForm
from .models import UserProfile


# Get redirect url from settings file or else redirect to admin page.
profile_redirect_url = settings.PROFILE_REDIRECT_URL or '/admin'
login_redirect_url = settings.LOGIN_REDIRECT_URL or ''


class Login(View):

    def get(self, request):
        """
        Return login template
        """
        if request.user.is_authenticated():
            return redirect(profile_redirect_url)
        import pdb; pdb.set_trace()
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        """
        Login user and redirect to Profile
        """
        form = LoginForm()
        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            return render(request, 'registration/login.html', {'errors': login_form.errors, 'form': form})
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            error = {'general_error': "user don't match"}
            return render(request, 'registration/login.html', {'errors': error, 'form': form})

        if user.check_password(password):
            login(request, user)
            return redirect(profile_redirect_url)
        error = {'general_error': "Passwords don't match"}
        return render(request, 'registration/login.html', {'errors': error, 'form': form})
        
class Signup(View):

    def get(self, request):
        """
        Return signup template
        """
        if request.user.is_authenticated():
            return redirect(login_redirect_url)
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        """
        Signup and redirect to Profile
        """
        form = SignupForm()
        signup_form = SignupForm(request.POST)
        if not signup_form.is_valid():
            return render(request, 'registration/signup.html', {'errors': signup_form.errors, 'form': form})
        first_name = signup_form.cleaned_data.get('first_name')
        last_name = signup_form.cleaned_data.get('last_name')
        username = signup_form.cleaned_data.get('username')
        email = signup_form.cleaned_data.get('email')
        password_1 = signup_form.cleaned_data.get('password_1')
        password_2 = signup_form.cleaned_data.get('password_2')
        mobile = signup_form.cleaned_data.get('mobile')
        if not password_1 == password_2:
            error = {'general_error': "Passwords don't match"}
            return render(request, 'registration/signup.html', {'errors': error, 'form': signup_form})
        try:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password_1)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.mobile = mobile
                user.save()
                user_profile, user_profile_create = UserProfile.objects.get_or_create(user=user)
                user_profile.mobile = mobile
                user_profile.save()
                login(request, user)
                return redirect(login_redirect_url)
            else:
                error = {'general_error': 'User already registered.'}
                return render(request, 'registration/signup.html', {'errors': error, 'form': signup_form})
        except Exception:
            error = {'general_error': 'Cannot create user at the moment..'}
            return render(request, 'registration/signup.html', {'errors': error, 'form': signup_form})



class Profile(View):

    def get(self, request):
        """
        Return Profile template
        """
        if not request.user.is_authenticated():
            return redirect(login_redirect_url)
        return render(request, 'registration/profile.html')

def logoutuser(request):
    logout(request)
    return redirect(login_redirect_url)

class UpdateProfile(View):
    
    def get(self,request):
        if not request.user.is_authenticated():
            return redirect(login_redirect_url)
        form = ProfileForm()
        profile_form = ProfileForm(request.POST or None, initial={'mobile':request.user.userprofile.mobile})
        return render(request, 'registration/update_profile.html', {'form': profile_form})

    def post(self,request):
        form = ProfileForm()
        profile_form = ProfileForm(request.POST)
        if not profile_form.is_valid():
            return render(request, 'registration/update_profile.html', {'errors': profile_form.errors, 'form': form})
        mobile = profile_form.cleaned_data.get('mobile')    
        user_update_profile, user_update_profile_create = UserProfile.objects.get_or_create(user=request.user)
        user_update_profile.mobile = mobile
        user_update_profile.save()
        return redirect(profile_redirect_url)

class ResetPassword(View):

    def get(self,request):
        form = ResetPasswordForm()
        return render(request, 'registration/reset_password.html', {'form': form})

    def  post(self,request):
        import pdb; pdb.set_trace()