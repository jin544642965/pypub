# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0003_projectconf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectconf',
            name='releases_num',
            field=models.IntegerField(),
        ),
    ]
