from django.contrib import admin
from .models import UserProfile,PasswordResetTokens


class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'mobile']
    search_fields = [('user', 'mobile')]

class PasswordResetTokensAdmin(admin.ModelAdmin):
    model = PasswordResetTokens
    list_display = ['user', 'token','expired_time']

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(PasswordResetTokens, PasswordResetTokensAdmin)
