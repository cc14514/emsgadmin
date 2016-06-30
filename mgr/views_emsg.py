#!/usr/bin/env python
# coding=utf8
from mgr.base import *

logger = logging.getLogger(__name__)


class EmsgAction(BaseAction):
    '''
    跟路径： /mgr/
    '''

    def uuid(self):
        return HttpResponse(uuid.uuid4().hex)

    def index(self):
        return self._response('mgr/index.html', {})

    def emsg(self):
        '''
        消息服务器，应用首页
        '''
        request = self.request
        datalist = []
        if self._in_group('user'):
            datalist = EmsgDomain.objects.filter(userid=request.user.username)
        elif self._in_group('admin'):
            datalist = EmsgDomain.objects.all()

        page = PageBean(datalist, request)
        # 新增加的 appkey 字段，得补上
        for po in page.data:
            if not po.appkey:
                domainConfig = EmsgDomainConfig.objects.filter(attr='license', domain=po.name)[0]
                po.appkey = domainConfig.value
                po.save()
        ctx = dict(page=page)
        return self._response('mgr/emsg/index.html', ctx)

    def emsg_domain_form(self):
        '''
        消息服务器，应用首页 > 新增／修改
        '''
        id = self._get_params('id')
        icon = self._get_params('icon')
        appkey = self._get_params('appkey')
        name = self._get_params('name')
        description = self._get_params('description')
        logger.debug('id=%s ; icon=%s ; appkey=%s ; name=%s ; desc=%s' % (id, icon, appkey, name, description))
        if self.request.method == 'GET':
            if not id:
                action = '新增'
                vo = None
                appkey = uuid.uuid4().hex
            else:
                action = '修改'
                vo = EmsgDomain.objects.get(id=id)
                appkey = vo.appkey
            ctx = dict(action=action, vo=vo, appkey=appkey)
            return self._response('mgr/emsg/domain_form.html', ctx)
        elif self.request.method == 'POST':
            if not id:
                # 新增
                po = EmsgDomain.objects.create(id=uuid.uuid4().hex)
                self._init_app_config(name)
            else:
                # 修改
                po = EmsgDomain.objects.get(id=id)
            po.appkey = appkey
            po.name = name
            po.description = description
            po.icon = icon
            po.userid = self.request.user.username
            po.save()
            # 调整配置
            if appkey:
                domainConfig = EmsgDomainConfig.objects.filter(attr='license', domain=name)[0]
                domainConfig.value = appkey
                domainConfig.save()
            return self._redirect('/mgr/emsg/')

    def emsg_check_domain(self):
        '''
        注册时，检测域名是否已存在
        '''
        self.request.GET
        name = self._get_params('name')
        try:
            domain = EmsgDomain.objects.get(name=name)
            rtn = 'false'
        except:
            rtn = 'true'
        return HttpResponse(rtn)

    def emsg_details(self):
        '''
        左右布局显示一个appname的详细信息
        '''
        try:
            menu = int(self._get_params('menu'))
        except:
            menu = 1
        if not menu or menu == 1:
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
        app_id = self._get_params('app_id')
        po = EmsgDomain.objects.get(id=app_id)
        ctx = dict(vo=po, )
        return self._response('mgr/emsg/details/menu_1.html', ctx)

    def emsg_details_menu_2(self):
        ''' 数据统计 '''
        app_id = self._get_params('app_id')
        po = EmsgDomain.objects.get(id=app_id)
        ctx = dict(vo=po, )
        return self._response('mgr/emsg/details/menu_2.html', ctx)

    def emsg_details_menu_3(self):
        ''' 在线用户 '''
        app_id = self._get_params('app_id')
        po = EmsgDomain.objects.get(id=app_id)

        request = self.request
        app_name = po.name
        pageNo = request.GET.get('pageNo')
        if not pageNo:
            pageNo = 0
        cfg = EmsgDomainConfig.objects.filter(domain=app_name, attr='license')[0]
        app_key = cfg.value
        logger.debug("app_name=%s ; app_key=%s" % (app_name, app_key))
        params = {'domain': app_name, 'license': app_key, 'pageSize': 10, 'pageNo': pageNo}
        success = self._emsg_service(service='emsg_status', method='get_user_list', params=params)
        logger.debug('app_main_user__success=%s' % success)
        su = success['success']
        entity = success['entity']
        page = {'totalCount': 0, 'pageSize': 20, 'pageNo': 0, 'result': []}
        if su:
            totalCount = entity['total_count']
            pageSize = entity['pageSize']
            pageNo = entity['pageNo']
            result = entity['result']
            totalNo = (totalCount + pageSize - 1) / pageSize
            page = {
                'totalCount': totalCount,
                'totalNo': totalNo,
                'lastPage': totalNo - 1,
                'pageSize': pageSize,
                'pageNo': pageNo + 1,
                'result': result,
                'next': pageNo + 1,
                'back': pageNo - 1,
            }
        logger.debug('app_main_user__page=%s' % page)
        ctx = {
            'app_name': app_name,
            'app_key': app_key,
            'page': page,
            'vo': po,
        }
        return self._response('mgr/emsg/details/menu_3.html', ctx)

    def emsg_details_menu_4(self):
        ''' 配置 '''
        app_id = self._get_params('app_id')
        logger.debug('app_id==>%s ; %s' % (app_id, self.request.method))
        po = EmsgDomain.objects.get(id=app_id)
        if self.request.method == 'GET':
            app_name = po.name
            ctx = {'app_name': app_name, 'sync': self.request.GET.get('sync'), 'vo': po}
            for dc in EmsgDomainConfig.objects.filter(domain=app_name):
                ctx[dc.attr] = dc.value
            for oc in EmsgOfflineConfig.objects.filter(domain=app_name):
                ctx[oc.attr] = oc.value
            logger.debug(ctx)
            return self._response('mgr/emsg/details/menu_4.html', ctx)
        elif self.request.method == 'POST':
            request = self.request
            sync = self._get_params('sync')
            logger.debug('poster==> %s' % request.POST)
            app_name = po.name
            ## emsgDomainConfig = EmsgDomainConfig(id=id,domain=app_name,attr=attr,value=val)
            self._set_domain_config(app_name, 'auth_enable', request.POST.get('auth_enable'))
            self._set_domain_config(app_name, 'http_callback_enable', request.POST.get('http_callback_enable'))
            self._set_domain_config(app_name, 'http_callback_url', request.POST.get('http_callback_url'))
            self._set_domain_config(app_name, 'offline_callback', request.POST.get('offline_callback'))
            self._set_offline_config(app_name, 'offline_ex', request.POST.get('offline_ex'))
            self._call_load_domains(app_name)
            return self._redirect('/mgr/emsg_details/', {'sync': sync, 'menu': 4, 'app_id': po.id})

    def emsg_details_menu_5(self):
        '''
        调试控制台
        '''
        app_id = self._get_params('app_id')
        po = EmsgDomain.objects.get(id=app_id)
        domain = po.name
        request = self.request
        query = {}
        from_jid, to_jid = '', ''

        from_jid = request.GET.get('from_jid')
        if from_jid and from_jid.endswith(domain):
            query.update({'from_jid': from_jid})
        else:
            query.update({'from_jid': {'$regex': domain}})

        to_jid = request.GET.get('to_jid')
        if to_jid and to_jid.endswith(domain):
            query.update({'to_jid': to_jid})
        else:
            query.update({'to_jid': {'$regex': domain}})

        dataList = []
        logger.debug("from=%s ; to=%s ; po.name=%s" % (from_jid, to_jid, po.name))
        db = conn['emsg']
        coll = db['emsg_log']
        if query or 'root' == request.user.username:
            logger.debug(query)
            dataList = coll.find(query, {'_id': 0}).sort("ts", pymongo.DESCENDING).skip(0).limit(100)
        ctx = {
            'from_jid': from_jid,
            'to_jid': to_jid,
            'dataList': dataList,
            'vo': po,
        }
        return self._response('mgr/emsg/details/menu_5.html', ctx)

    def _init_app_config(self, app_name):
        '''
        创建应用时，用来初始化配置
        '''
        for esc in EmsgSysConfig.objects.all():
            id = uuid.uuid4().hex
            (attr, val) = (esc.attr, esc.value)
            emsgDomainConfig = EmsgDomainConfig.objects.create(id=id, domain=app_name, attr=attr, value=val)
            emsgDomainConfig.save()
            logger.debug("=====> attr=%s ; val=%s " % (attr, val))

    def _emsg_service(self, service, method, params):
        sn = uuid.uuid4().hex
        body = {'sn': sn, 'service': service, 'method': method, 'params': params}
        body = json.dumps(body)
        logger.debug("emsg_serice__body=%s" % body)
        data = urllib.urlencode({'body': body})
        req = urllib2.Request(url=settings.emsg_service_url, data=data)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        logger.debug("emsg_serice__response=%s" % res)
        return json.loads(res)

    def _call_load_domains(self, app_name):
        ''' 重新加载配置 '''
        self._emsg_service(service='emsg_config_domain', method='load_domains', params={'domainList': [app_name]})
        self._emsg_service(service='emsg_config_offline', method='load_domains', params={'domainList': [app_name]})

    def _set_domain_config(self, app_name, attr_name, value):
        if value:
            c = EmsgDomainConfig.objects.filter(domain=app_name, attr=attr_name)
            if c:
                obj = c[0]
                obj.value = value
            else:
                obj = EmsgDomainConfig.objects.create(id=uuid.uuid4().hex, domain=app_name, attr=attr_name, value=value)
            obj.save()

    def _set_offline_config(self, app_name, attr_name, value):
        if value:
            c = EmsgOfflineConfig.objects.filter(domain=app_name, attr=attr_name)
            if c:
                obj = c[0]
                obj.value = value
            else:
                obj = EmsgOfflineConfig.objects.create(id=uuid.uuid4().hex, domain=app_name, attr=attr_name,
                                                       value=value)
            obj.save()
