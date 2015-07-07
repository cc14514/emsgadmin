#!/usr/bin/env python
#coding=utf-8

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login,logout
from django.views.generic import RedirectView  

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'emsgadmin.views.home', name='home'),
    # url(r'^emsgadmin/', include('emsgadmin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	('^accounts/login/$',login,{'template_name':'login.html'}),
	('^accounts/logout/$',logout,{'template_name':'login.html','next_page':'/'}),
	#('^$' 			,'emsgadmin.admin.views.main'),
	('^rest/$' 		,'emsgadmin.admin.views.rest'),
	('^app_save/$' 	,'emsgadmin.admin.views.app_save'),

	('^app_main/$' 				,'emsgadmin.admin.views.app_main'),
	('^app_main/statistic/$' 	,'emsgadmin.admin.views.app_main_statistic'),
	('^app_main/user/$' 		,'emsgadmin.admin.views.app_main_user'),
	('^app_main/config/$' 		,'emsgadmin.admin.views.app_main_config'),
    ('^app_main/config_save/$'     ,'emsgadmin.admin.views.app_main_config_save'),
    ('^app_main/log/$'     ,'emsgadmin.admin.views.app_main_log'),
    
    # 管理控制台
    ('^$',RedirectView.as_view(url='/mgr/emsg/')),
    url(r'^mgr/',include('mgr.urls')),
    (r'^uploadify/$','emsgadmin.views.uploadify'),
)
