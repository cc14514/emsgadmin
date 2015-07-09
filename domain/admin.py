#/usr/bin/env python
#coding=utf8

from django.contrib import admin
from domain.models import *

class EmsgDomainAdmin(admin.ModelAdmin):
    list_display = ('name','appkey','userid','description') 
    fields = ('id','name','appkey','userid','description') 
    list_filter = ('userid',)
    search_fields = ('name', 'userid')

admin.site.register(EmsgDomain,EmsgDomainAdmin)


class FileserverCfgAdmin(admin.ModelAdmin):
    list_display = ('appid','appkey','userid','description') 
    fields = ( 'appid','appkey','userid','description') 
    list_filter = ('userid',)
    search_fields = ('appid', 'userid')

admin.site.register(FileserverCfg ,FileserverCfgAdmin)