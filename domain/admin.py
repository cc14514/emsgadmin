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
    list_display = ('appid','appkey','icon','userid','description') 
    fields = ( 'appid','appkey','icon','userid','description') 
    list_filter = ('userid',)
    search_fields = ('appid', 'userid')

admin.site.register(FileserverCfg ,FileserverCfgAdmin)

class FileserverNodesAdmin(admin.ModelAdmin):
    list_display = ('comment','host','port') 
    fields = ('comment','host','port') 

admin.site.register(FileserverNodes ,FileserverNodesAdmin)