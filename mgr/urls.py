# /usr/bin/env python
# coding=utf8
from django.conf.urls import patterns
from django.views.generic import RedirectView

urlpatterns = patterns('',

                       (r'^(?P<m>\w+)/$', 'mgr.views.emsg'),
                       (r'^fileserver/(?P<m>\w+)/$', 'mgr.views.fileserver'),

                       )
