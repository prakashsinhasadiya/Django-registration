
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, null=True, blank=True)


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.now() + timedelta(hours=24)

class PasswordResetTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField("Tocken ID", max_length=60, null=False, blank=False)
    expired_time = AutoDateTimeField(default=datetime.now)
    # used = models.BooleanField(default=False)