from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'mobile']
    search_fields = [('user', 'mobile')]


admin.site.register(UserProfile, ProfileAdmin)
