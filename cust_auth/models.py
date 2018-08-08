
from datetime import datetime, timedelta
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex],max_length=17)

class PasswordResetTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField("Tocken ID", max_length=60, null=False, blank=False)