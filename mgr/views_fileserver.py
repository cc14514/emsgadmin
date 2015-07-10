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

    
    def emsg_details_menu_2(self):
        ''' 数据统计 '''
        app_id = self._get_params('app_id' )
        logger.debug(app_id)
        ctx = dict(vo=FileserverCfg.objects.get(id=app_id),)
        return self._response('mgr/fileserver/details/menu_2.html',ctx)

    def emsg_details_menu_3(self):
        ''' 文件管理 '''
        app_id = self._get_params('app_id' )
        po = FileserverCfg.objects.get(id=app_id)
        appid = po.appid
        appkey = po.appkey
        pageNo = self._get_params('pageNo')
        ct = self._get_params('ct')
        pageSize = 20

        if not pageNo :
            pageNo = 0
        else:
            pageNo = int(pageNo)
        
        condition = {'appid':appid}
        if ct:
            condition['ct'] = {"$regex":ct}
            
        db = conn['fileserver']
        coll = db['fileindex']
        logger.debug('condition=%s' % condition)
        totalCount = coll.find(condition,{"_id":0}).count()
        datalist = coll.find(condition,{"_id":0}).skip(pageNo*pageSize).limit(pageSize).sort("ct",pymongo.DESCENDING)
        result = []
        for data in datalist:
            if data.has_key('auth'):
                auth = str(data.get('auth'))
                if auth == 'true' or auth=='True':
                    data['auth'] = True
                else:
                    data.pop('auth')
            if data.has_key('size'):
                size = data.get('size')
                size = int(size)/1000
                if size>1000:
                    size = '%s M' % size/1000 
                else:
                    size = '%s K' % size 
                data['size'] = size
            data['href'] = self._get_file(pk=data.get('pk'),auth=data.get('auth'),appid=appid,appkey=appkey)
            result.append(data)
        totalNo = (totalCount+pageSize-1)/pageSize
        page = {
            'totalCount':totalCount,
            'totalNo':totalNo,
            'lastPage':totalNo-1,
            'pageSize':pageSize,
            'pageNo':pageNo+1,
            'result':result,
            'next':pageNo+1,
            'back':pageNo-1,
        }
        logger.debug('fileserver__page=%s' % page)    
        ctx = { 
            'page':page,
            'condition':condition,
            'vo':po,
        }    
        return self._response('mgr/fileserver/details/menu_3.html',ctx)
    
    def del_file(self):
        '''
        ajax 删除文件
        '''
        app_id = self._get_params('app_id' )
        po = FileserverCfg.objects.get(id=app_id)
        pk = self._get_params('pk' )
        auth = self._get_params('auth' )
        logger.debug('del_file pk=%s ; auth=%s ; app_id=%s' % (pk,auth,app_id))
        appid = po.appid
        appkey = po.appkey
        # 调用删除接口
        url = settings.fileserver_service_url
        url_token = urlparse.urljoin(url,'/fileserver/token/')
        url_del = urlparse.urljoin(url,'/fileserver/del/')
        
        if auth:
            # 非公开的文件删除时，需要先得到 token ，否则无法完成删除
            form = dict(appid=appid,appkey=appkey)
            rtn = poster.submit(url_token,form)
            logger.debug('token_rtn=%s' % rtn)
            if rtn.get('success'):
                # 拿到 token
                token = rtn.get('entity').get('token')
                form = dict(id=pk,token=token)
                rtn = poster.submit(url_del,form)
                logger.debug('del_token_rtn=%s' % rtn)
            else:
                return HttpResponse('{"success":false,"entity":{"reason":"get token error"}}',content_type="text/json ; charset=utf8")
        else:
            # 删除公开资源时，直接删除即可    
            form = dict(id=pk,appid=appid,appkey=appkey)
            rtn = poster.submit(url_del,form)
            logger.debug('del_rtn=%s' % rtn)
        return HttpResponse('{"success":true,"entity":"%s"}' % pk,content_type="text/json ; charset=utf8")

    def _get_file(self,**args):
        '''
        拼出获取文件的url
        '''
        pk,appid,appkey,auth = args['pk'],args['appid'],args['appkey'],args['auth']
        # 调用接口
        url = settings.fileserver_service_url
        url_token = urlparse.urljoin(url,'/fileserver/token/')
        url_get = urlparse.urljoin(url,'/fileserver/get/%s/' % pk)
        if auth:
            # 非公开的文件删除时，需要先得到 token ，否则无法完成删除
            form = dict(appid=appid,appkey=appkey)
            rtn = poster.submit(url_token,form)
            logger.debug('token_rtn=%s' % rtn)
            if rtn.get('success'):
                # 拿到 token
                token = rtn.get('entity').get('token')
                return '%s?token=%s' % (url_get,token)
            else:
                return "#"
        else:
            # 获取公开资源时，直接获取即可    
            return url_get


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
            
