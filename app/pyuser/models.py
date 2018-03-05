# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)  #关联自带的User结构
    user_role = models.CharField(max_length=40)
    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()
