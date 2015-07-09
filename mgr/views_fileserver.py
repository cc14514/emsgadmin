#!/usr/bin/env python
# coding=utf8

from mgr.base import *

import urlparse
import pymongo
MONGO_HOST = settings.mongo_host
MONGO_PORT = settings.mongo_port
MONGO_REPLICASET = settings.mongo_replicaset
conn = pymongo.MongoClient(host=MONGO_HOST,port=MONGO_PORT,replicaset=MONGO_REPLICASET)

logger = logging.getLogger(__name__)


class FileserverAction(BaseAction):
    '''
    跟路径： /mgr/fileserver/
    '''
    def uuid(self): return HttpResponse(uuid.uuid4().hex)

    def index(self):
        '''
        消息服务器，应用首页
        '''
        request = self.request
        datalist = [] 
        if self._in_group('user'):
            datalist = FileserverCfg.objects.filter(userid=request.user.username)
        elif self._in_group('admin'):
            datalist = FileserverCfg.objects.all()

        page = PageBean(datalist, request)
        ctx = dict(page=page)
        return self._response('mgr/fileserver/index.html',ctx) 
       
    def app_form(self): 
        id = self._get_params('id')
        icon = self._get_params('icon')
        appid = self._get_params('appid')
        appkey = self._get_params('appkey')
        description = self._get_params('description')
        logger.debug('id=%s ; icon=%s ; appkey=%s ; appid=%s ; desc=%s' % (id,icon,appkey,appid,description) )
        if self.request.method == 'GET':
            if not id : 
                action = '新增'
                vo = None
                appkey = uuid.uuid4().hex 
            else : 
                action = '修改' 
                vo = FileserverCfg.objects.get(id=id)
                appkey = vo.appkey
            ctx = dict(action=action,vo=vo,appkey=appkey)
            return self._response('mgr/fileserver/app_form.html',ctx) 
        elif self.request.method == 'POST':
            # 先提交请求，再回调同步，因为操作的是同一个库,同步前必须完成事务
            with transaction.commit_on_success():
                if not id :
                    # 新增
                    po = FileserverCfg.objects.create()
                else:
                    # 修改
                    po = FileserverCfg.objects.get(id=id)
                po.appid = appid 
                po.appkey = appkey
                po.description = description
                po.icon = icon
                po.userid = self.request.user.username 
                po.save()
            # 同步配置
            self._sync_app_config(appid)
            return self._redirect('/mgr/fileserver/index/')
    
    def check_appid(self):
        '''
        检测appid是否已存在
        '''
        appid = self._get_params('appid')
        try :
            logger.debug(appid)
            cfg = FileserverCfg.objects.get(appid=appid)
            rtn = 'false' 
        except:
            rtn = 'true' 
        return HttpResponse(rtn)
    

    def details(self):
        '''
        左右布局显示一个appname的详细信息
        '''
        try:
            menu = int(self._get_params('menu'))
        except:
            menu = 1
        if not menu or menu==1:
            return self.emsg_details_menu_1()
        elif menu == 2:
            return self.emsg_details_menu_2()
        elif menu == 3:
            return self.emsg_details_menu_3()
        elif menu == 4:
            return self.emsg_details_menu_4()
        elif menu == 5:
            return self.emsg_details_menu_5()

    def emsg_details_menu_1(self):
        ''' 基本信息 '''
        app_id = self._get_params('app_id' )
        po = FileserverCfg.objects.get(id=app_id)
        ctx = dict(vo=po,)
        return self._response('mgr/fileserver/details/menu_1.html',ctx)

    def _sync_app_config(self,appid):
        #TODO 同步配置到 fileserver
        token = 'u8_58zr6rjgd-qhicj#w7#jq*-*4%&%@jt=7&b!f+zi7#o0m8%'
        try:
            url = settings.fileserver_service_url
            url = urlparse.urljoin(url,'/callback/reload_cfg/')
            form = dict(appid=appid,token=token)
            rtn = poster.submit(url,form)
            logger.debug('fileserver_callback_success appid=%s ; rtn=%s' % (appid,rtn))
        except Exception as e:
            logger.error('fileserver_callback_error appid=%s ; e=%s' % (appid,e))
            
