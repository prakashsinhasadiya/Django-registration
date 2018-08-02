# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import Login, Signup,Profile
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^profile/$',Profile.as_view(), name='Profile')
]
