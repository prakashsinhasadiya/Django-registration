# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.http import Http404
from .forms import LoginForm, SignupForm,ProfileForm,ResetPasswordForm,ConfirmPasswordForm
from .models import UserProfile,PasswordResetTokens
import uuid



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
        reset_password_form = ResetPasswordForm(request.POST)
        if not reset_password_form.is_valid():
            return render(request, 'registration/reset_password.html', {'form': reset_password_form, 'errors': reset_password_form.errors})
        username = reset_password_form.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            return render(request, 'registration/reset_password.html', {'form': reset_password_form, 'errors': {'general_error': 'User doesnot exist.'}})
        token_obj = PasswordResetTokens.objects.create(
            user=user[0], token=uuid.uuid4().hex)
        url = ''
        url += request.get_host()
        url += '/set_password/'
        url += '?token=' + token_obj.token
        message = render_to_string('registration/reset_password_email_template.html', {
            'user': user[0],
            'url': url
        })
        res = send_mail('Password Reset', message, settings.FROM_EMAIL, [user[0].email])
        return render(request, 'registration/reset_email_sent.html')

class SetPassword(View):

    def get(self, request):
        """
        Check if authorized to reset password.
        Return reset password template
        """
        form = ConfirmPasswordForm()
        token = request.GET.get('token')
        if not token:
            raise Http404('Page not found.')
        token_obj = PasswordResetTokens.objects.filter(token=token)
        if not token_obj:
            raise Http404('Fake token supplied.')
        # if token_obj[0].used:
        #     raise Http404('Token already used')
        # tz = pytz.timezone("UTC")
        # if tz.localize(datetime.now(), is_dst=None) > token_obj[0].expiry_time:
        #     raise Http404('Token Expired. Try again')
        return render(request, 'registration/set_password.html', {'form': form, 'token': token})

    def post(self, request):
        """
        Save new password and redirect to Login
        """
        form = ConfirmPasswordForm(request.POST)
        token = request.POST.get('token')
        if not token:
            raise Http404('Page not found.')
        if not form.is_valid():
            return render(request, 'registration/set_password.html', {'form': form, 'token': token, 'errors': form.errors})
        token_obj = PasswordResetTokens.objects.filter(token=token)
        if not token_obj:
            raise Http404('Fake token supplied.')
        # if token_obj[0].used:
        #     raise Http404('Token already used')
        # tz = pytz.timezone("UTC")
        # if tz.localize(datetime.now(), is_dst=None) > token_obj[0].expiry_time:
        #     raise Http404('Token Expired. Try again')
        password_1 = form.cleaned_data.get('password_1')
        password_2 = form.cleaned_data.get('password_2')
        if not password_1 == password_2:
            return render(request, 'registration/set_password.html', {'form': form, 'token': token, 'errors': {'general_error': "passwords don't match"}})
        import pdb; pdb.set_trace()
        user = token_obj[0].user
        user.set_password(password_1)
        user.save()
        token_obj[0].used = True
        token_obj[0].save()
        return HttpResponseRedirect(reverse('login'))
