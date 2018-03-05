# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.pyuser.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = UserProfile
    #fk_name = 'user'
    max_num = 1
    can_delete = False

# class CustomUserAdmin(UserAdmin):
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)