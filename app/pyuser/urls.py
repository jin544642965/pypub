from django.conf.urls import url, include
from app.pyuser.views import *
urlpatterns = [
    url(r'^register/$', register),
    url(r'^logout/$',logout_view),
    url(r'^reset_password/$', reset_password),
    url(r'^active_user/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', active_user),
    url(r'^submit_email/$', submit_email),
    url(r'^change_pwd/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', change_pwd),
    url(r'change_password/$', change_password),
    url(r'user_list/$', user_list),
    url(r'user_add/$', user_add),
    url(r'user_del$', user_del),
    url(r'user_edit$',user_edit),
]