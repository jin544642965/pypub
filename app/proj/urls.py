from django.conf.urls import url, include
from app.proj.views import *

urlpatterns = [
    url(r'^conf/$', proj_conf),
    url(r'^add/$', proj_add),
    url(r'^edit$', proj_edit),
    url(r'^del$', proj_del),
    url(r'copy$', proj_copy),
    url(r'member$',proj_member),
]
