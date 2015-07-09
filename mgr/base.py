#!/usr/bin/env python
# coding=utf8
import logging, traceback, json, uuid, collections, urllib, urllib2, datetime
from django.template.loader import get_template  
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, Template
from django.template import RequestContext
from django.db import transaction
#需要跳过 csrf_token 的 post 时，用这个 注解
from django.views.decorators.csrf import csrf_exempt
from domain.models import *
import billiard
import urllib
import requests
from myTags.utils import *
from myTags.pageBean import *
from myTags import poster

from emsgadmin import settings

import pymongo
MONGO_HOST = settings.mongo_host
MONGO_PORT = settings.mongo_port
MONGO_REPLICASET = settings.mongo_replicaset
conn = pymongo.MongoClient(host=MONGO_HOST,port=MONGO_PORT,replicaset=MONGO_REPLICASET)


logger = logging.getLogger(__name__)

class BaseAction(object):
    '''
    fma 基类,m 表示 method ,a 为 args，request 包含了参数
    用 render 执行method，并返回对应的页面
    '''
    def __init__(self,request,m=None):
        self.request = request
        self.m = m
    def render(self):
        try:
            mtd = getattr(self,self.m)
            return mtd() # call def
        except Exception as e:
            logger.debug("############")
            logger.error(e)
            logger.debug("############")
            s = traceback.format_exc()
            logger.error(s)
            return render_to_response('mobile/500.html',{'exception':e},context_instance=RequestContext(self.request))
    
    def _response(self,template,ctx):
        logger.debug('response__user=%s' % self.request.user)
        return render_to_response(template,ctx,context_instance=RequestContext(self.request))
    def _redirect(self,url,ctx={}):
        if ctx:
            params = urllib.urlencode(ctx)
            return HttpResponseRedirect('%s?%s' % (url,params))
        else:
            return HttpResponseRedirect(url)
    def _recv_file(self,file_name):
        '''
        接收 图片上传
        '''
        request = self.request
        logger.debug(request.FILES)
        if file_name in request.FILES:
            uf = request.FILES[file_name]
            path = os.path.join('/tmp', uuid.uuid4().hex)
            outputStream = open(path,'wb+')
            for chunk in uf.chunks():
                outputStream.write(chunk)
            outputStream.close()
            success = fileserver_client.upload(file_path=path)
            return success
        return {'success':False}
    
    def _get_params(self,key,default=None):
        '''
        获取参数
        '''
        request = self.request
        if request.method=='GET':
            val = request.GET.get(key)
        elif request.method=='POST':
            val = request.POST.get(key)
        else:
            return None
        if not val and default :
            return default
        else:
            return val

    def _in_group(self,name): 
        ''' 是否包含在指定的 组 内 '''
        try:
            user = self.request.user
            logger.debug('group_name=%s ; user=%s' % (name,user.username))
            user.groups.get(name=name)
            return True
        except:
            return False
