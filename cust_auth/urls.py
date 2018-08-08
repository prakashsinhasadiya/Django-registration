# -*- coding: utf-8 -*-
import os


from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import (
	Login, Signup,
	Profile,logoutuser,
	UpdateProfile,ResetPassword,SetPassword
)

urlpatterns = [
    url(r'^$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^profile/$',Profile.as_view(), name='profile'),
    url(r'^logout/$',logoutuser,name="logout"),
    url(r'^update_profiles/$',UpdateProfile.as_view(),name="update_profile"),
    url(r'^reset_password/$',ResetPassword.as_view(),name="reset_password"),
    url(r'^set_password/$', SetPassword.as_view(), name='set_password'),

]
