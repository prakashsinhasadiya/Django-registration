# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-07 06:09
from __future__ import unicode_literals

import cust_auth.models
import datetime
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cust_auth', '0003_passwordresettokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresettokens',
            name='expired_time',
            field=cust_auth.models.AutoDateTimeField(default=datetime.datetime(2018, 8, 7, 6, 9, 5, 971101)),
        ),
    ]