# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 03:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0007_auto_20170503_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
