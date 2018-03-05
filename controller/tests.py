# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import json

from django.conf import settings
from django.core.cache import cache

# Create your tests here.

def read_from_cache(self,useremail):
    key = 'session_id_t_' + useremail
    value =cache.get(key)
    if value == None:
        data = None
    else:
        data = json.loads(value)
    return data

def write_to_cache(self,useremail):
    key = 'session_id_t_' + useremail
    cache.set(key,json.dumps(useremail),settings.NEVER_REDIS_TIMEOUT)

