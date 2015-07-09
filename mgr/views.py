#!/usr/bin/env python
# coding=utf8
from mgr.views_emsg import *
from mgr.views_fileserver import *

logger = logging.getLogger(__name__)
########################################################################
## 入口函数 
########################################################################
@login_required
@csrf_exempt
def emsg(request,m):
    ''' 消息服务器入口函数 '''
    logger.debug('emsg  m=%s ; %s ; user=%s' % (m,request.method,request.user.username))
    return EmsgAction(request,m).render()

@login_required
@csrf_exempt
def fileserver(request,m):
    ''' 文件服务器入口函数 '''
    logger.debug('fileserver  m=%s ; %s ; user=%s' % (m,request.method,request.user.username))
    return FileserverAction(request,m).render()
