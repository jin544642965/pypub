# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class ProjectConf(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=20)
    env = models.CharField(max_length=20)
    submit_method = models.CharField(max_length=20)
    repo_address = models.CharField(max_length=100)
    p_username = models.CharField(max_length=20)
    p_password = models.CharField(max_length=20)
    repertory = models.CharField(max_length=100)
    excludes_file = models.TextField(max_length=256)
    www_user = models.CharField(max_length=20)
    web_path = models.CharField(max_length=20)
    deploy_releases = models.CharField(max_length=20)
    releases_num = models.IntegerField()
    servers = models.TextField(max_length=256)


    def __unicode__(self):
        return self.project_name
