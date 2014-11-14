#!/usr/bin/env python
#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import logging,traceback,json,uuid,collections,urllib,urllib2,datetime
from emsgadmin.admin.models import *
import emsgadmin.settings as settings

from emsgadmin.emsg_inf_push import emsg_inf_push 
from emsgadmin.emsg_inf_push import ttypes 
from emsgadmin.emsg_inf_push import constants 

from thrift import Thrift 
from thrift.transport import TSocket 
from thrift.transport import TTransport 
from thrift.protocol import TBinaryProtocol

logger = logging.getLogger(__name__)

@login_required
def main(request):
	'''
	应用管理页面
	'''
	logger.debug('main__page__open')	
	domain_list = EmsgDomain.objects.filter(userid=request.user.username)
	logger.debug("============ %s =============" % request.user.username)
	ctx = {
		'domain_list':domain_list,
		'is_root':'admin'==request.user.username,
	}
	call_load_domains_on_view(request)
	return render_to_response('index.html',ctx,context_instance=RequestContext(request))	

@login_required
def app_main(request):
	app_name = request.GET.get('app_name')
	c = EmsgDomainConfig.objects.filter(domain=app_name,attr='license')
	# 如果没有 app_key 就用uuid创建一个
	if c :
		cfg = c[0]
		app_key = cfg.value
	else:
		id = uuid.uuid4().hex
		emsgDomainConfig = EmsgDomainConfig(id=id,domain=app_name,attr='license',value=id)
		emsgDomainConfig.save()
		app_key = id
	ctx = { 
		'app_name':app_name,
		'app_key':app_key,
	}	
	return render_to_response('app_main.html',ctx,context_instance=RequestContext(request))	

@login_required
def app_main_statistic(request):
	app_name = request.GET.get('app_name')
	ctx = { 'app_name':app_name }	
	return render_to_response('app_main_statistic.html',ctx,context_instance=RequestContext(request))	

@login_required
def app_main_user(request):
	app_name = request.GET.get('app_name')
	pageNo = request.GET.get('pageNo')
	if not pageNo :
		pageNo = 0
	cfg = EmsgDomainConfig.objects.filter(domain=app_name,attr='license')[0]
	app_key = cfg.value
	logger.debug("app_name=%s ; app_key=%s" % (app_name,app_key))
	params = {'domain':app_name,'license':app_key,'pageSize':10,'pageNo':pageNo}
	success = emsg_service(service='emsg_status',method='get_user_list',params=params)
	logger.debug('app_main_user__success=%s' % success)
	su = success['success']
	entity = success['entity']
	page = { 'totalCount':0, 'pageSize':20, 'pageNo':0, 'result':[]}
	if su :
		totalCount = entity['total_count']	
		pageSize = entity['pageSize']	
		pageNo = entity['pageNo']	
		result = entity['result']	
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
	logger.debug('app_main_user__page=%s' % page)	
	ctx = { 
		'app_name':app_name,
		'app_key':app_key,
		'page':page
	}	
	return render_to_response('app_main_user.html',ctx,context_instance=RequestContext(request))	

@login_required
def app_main_config(request):
	app_name = request.GET.get('app_name')
	ctx = { 'app_name':app_name,'sync':request.GET.get('sync') }	
	for dc in EmsgDomainConfig.objects.filter(domain=app_name):
		ctx[dc.attr] = dc.value
	for oc in EmsgOfflineConfig.objects.filter(domain=app_name):
		ctx[oc.attr] = oc.value
	logger.debug(ctx)
	call_load_domains_on_view(request)
	return render_to_response('app_main_config.html',ctx,context_instance=RequestContext(request))	

@login_required
def app_main_config_save(request):
	logger.debug(request)
	app_name = request.POST.get('app_name')
	## emsgDomainConfig = EmsgDomainConfig(id=id,domain=app_name,attr=attr,value=val)
	
	set_domain_config(app_name,'auth_enable',request.POST.get('auth_enable'))
	set_domain_config(app_name,'http_callback_enable',request.POST.get('http_callback_enable'))
	set_domain_config(app_name,'http_callback_url',request.POST.get('http_callback_url'))
	set_domain_config(app_name,'offline_callback',request.POST.get('offline_callback'))
	set_offline_config(app_name,'offline_ex',request.POST.get('offline_ex'))
	
	return HttpResponseRedirect('/app_main/config/?app_name=%s&sync=%s' % (app_name,app_name))
@login_required
def app_save(request):
	'''
	保存要添加的域名
	'''
	id = request.POST.get('id')
	if id :
		modify = True 
	else :
		modify = False
		id = uuid.uuid4().hex
	name = request.POST.get('name')
	description = request.POST.get('description')
	username = request.user.username
	if modify :
		pass
	else :		
		emsgDomain = EmsgDomain(id=id,name=name,userid=username,description=description)
		emsgDomain.save()
		init_app_config(name)

	logger.debug("::::::::: name=%s ; description=%s" % (name,description))
	return HttpResponseRedirect('/?sync=%s' % name)

def rest(request):
	'''
	urls.py 中配置了 /rest 转向到此方法,转发所有的rest请求
	输入: body={"method":"已注册的方法","params":{...参数...}}
	输出: {"success":true/false,"entity":{...}}
	'''
	try :
		if 'GET' == request.method :
			body = request.GET.get('body')
		elif 'POST' == request.method:
			body = request.POST.get('body')
		logger.debug("::::::::body=%s ;" % (body))
		body = json.loads(body)
		method = body['method']
		params = body['params']
		success = apply(rest_map[method],(),{'params':params})	
	except :
		success = {'success':False}
	return HttpResponse(json.dumps(success),content_type="text/json ; charset=utf8")


##################################
## rest_handler
##################################
def init_app_config(app_name):
	for esc in EmsgSysConfig.objects.all() :
		id = uuid.uuid4().hex
		(attr,val) = (esc.attr,esc.value)
		if attr == 'license' :
			val = uuid.uuid4().hex
		emsgDomainConfig = EmsgDomainConfig(id=id,domain=app_name,attr=attr,value=val)
		emsgDomainConfig.save()
		logger.debug("=====> attr=%s ; val=%s " % (attr,val))



##################################
## rest_handler
##################################

# 校验要创建的域是否存在
def checkappname(params):			
	'''
	校验要创建的域是否存在
	输入: 要教研的string
	输出: success
	'''
	if EmsgDomain.objects.filter(name=params) :
		return success(False,"already_exist")
	else:
		return success(True) 
def checkusername(params):			
	'''
	教研用户是否已经存在
	输入: 要教研的string
	输出: success
	'''
	if User.objects.filter(username=params) :
		return success(False,"already_exist")
	else:
		return success(True) 

def statistic_1(params):
	'''
	统计一天的在线用户数，以小时为最小单位
	获取 params 指定的日期的在线用户数据
	params 格式　yy-mm-dd
	'''
	logger.debug("statistic_1__request=%s" % params)
	if not params['condition']:
		params['condition'] = '%s' % datetime.date.today() 
		logger.debug("statistic_1__default_request=%s" % params)
	hourlyList = EmsgStatSessionHourly.objects.filter(
            domain=params['app_name'],
            time__startswith=params['condition']
        ).order_by('time')

	data = {}
	hours = ["%02d" % k for k in range(24)]
	for hour in hours:
		data[hour] = 0

	if hourlyList:
		for hourly in hourlyList:
			k = hourly.time.split('-')[-1]
			data[k] = hourly.total_count
	return success(True,{'params':params,'data':chart_data_1(data)})

def statistic_2(params):
	'''
	统计指定时间段的在线用户数，以天为最小单位
	获取 params 指定的日期的在线用户数据
	params 格式　yy-mm-dd
	'''
	logger.debug("statistic_2__request=%s" % params)
	timespan = int(params['condition'])
	today = datetime.date.today() 
	befor = today - datetime.timedelta(timespan)
	logger.debug("statistic_2__default_request today=%s ; befor=%s" % (today,befor))
	dailyList = EmsgStatSessionDaily.objects.filter(
		domain=params['app_name'],
		time__lte=str(today),
		time__gte=str(befor)
	).order_by('time')

	data = {}
	for k in range(timespan):
		date = today - datetime.timedelta(k);
		data[date.strftime('%Y-%m-%d')] = 0

	for daily in  dailyList :
		data[daily.time] = daily.total_count
	return success(True,chart_data_1(data))

def reg_save(params):
	'''
	注册一个用户
	'''
	logger.debug("=============== %s" % params)
	f = (username,password,email) = (
		params.get('username'),
		params.get('password'),
		params.get('email')
	)
	user = User.objects.create_user(username=username,password=password,email=email)
	user.is_staff = True
	user.save()
	logger.debug("::::::::: reg_form=%s" % list(f))
	return success(True)

def send_packet(params):
    '''
    params 包含如下属性
        from,to,payload,app_key
    '''
    sn = uuid.uuid4().hex
    payload = params['payload'] 
    try:
    	payload = json.loads(payload)
    except:
    	pass
    packet = {
        'envelope':{
            'id':sn,
            'type':1,
            'ack':1,
            'from':params['from'],
            'to':params['to'],
        },        
        'payload':payload,
        'vsn':'0.0.1'
    }
    logger.debug("sending__%s" % packet)
    host,port = settings.emsg_inf_push_host,settings.emsg_inf_push_port 
    transport = TSocket.TSocket(host , port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = emsg_inf_push.Client(protocol)
    transport.open()
    client.process(params['app_key'],sn,json.dumps(packet) )
    transport.close()
    return success(True)

# 注册 rest 方法
rest_map = {
	'checkappname':checkappname,				
	'checkusername':checkusername,
	'statistic_1':statistic_1,				
	'statistic_2':statistic_2,				
	'reg_save':reg_save,				
	'send_packet':send_packet,				
}
# 封装返回值
def success(isOk,entity={}): 
	if isOk : 
		res = {'success':isOk,'entity':entity} 
	else: 
		res = {'success':isOk,'entity':{'reason':entity}} 
	logger.info('response=%s' % res) 
	return res



##################################
## private methods 
##################################

def emsg_service(service,method,params,sn=uuid.uuid4().hex):
	body={'sn':sn,'service':service,'method':method,'params':params}
	body = json.dumps(body)
	logger.debug("emsg_serice__body=%s" % body)
	data = urllib.urlencode({'body':body})
	req = urllib2.Request(url = settings.emsg_service_url,data = data)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	logger.debug("emsg_serice__response=%s" % res)
	return json.loads(res)

def call_load_domains(app_name):
	emsg_service(service='emsg_config_domain',method='load_domains',params={'domainList':[app_name]})
	emsg_service(service='emsg_config_offline',method='load_domains',params={'domainList':[app_name]})

def call_load_domains_on_view(request):
	if 'GET' == request.method :
		sync = request.GET.get('sync') 
	elif 'POST' == request.method:
		sync = request.POST.get('sync') 
	if sync :
		logger.debug("sync=%s" % sync)
		call_load_domains(sync)

def set_offline_config(app_name,attr_name,value):
	if value :
		c = EmsgOfflineConfig.objects.filter(domain=app_name,attr=attr_name)
		if c :
			obj = c[0]
			obj.value = value 
		else:
			obj = EmsgOfflineConfig(id=uuid.uuid4().hex,domain=app_name,attr=attr_name,value=value)
		obj.save()
def set_domain_config(app_name,attr_name,value):
	if value :
		c = EmsgDomainConfig.objects.filter(domain=app_name,attr=attr_name)
		if c :
			obj = c[0]
			obj.value = value 
		else:
			obj = EmsgDomainConfig(id=uuid.uuid4().hex,domain=app_name,attr=attr_name,value=value)
		obj.save()

def chart_data_1(data_map):
	'''
	构造图标数据，只有一条线的图表数据
	data_map format {x0:y0,x1:y1,...}
	'''
	# 按照key排序，有序字典
	d = collections.OrderedDict( sorted( data_map.items(), key=lambda t:t[0] ) )
	labels = d.keys() 
	values = d.values()
	logger.debug(labels)
	logger.debug(values)
	data = {
		'labels' : labels,
		'datasets' : [ { 
			'fillColor': "rgba(220,220,220,0.5)", 
			'strokeColor': "rgba(220,220,220,1)", 
			'pointColor': "rgba(220,220,220,1)", 
			'pointStrokeColor': "#fff", 
			'data': values 
		} ] 
	}
	logger.debug('response_dict=%s' % data)
	return data 

    
# def send_packet(params):
#     '''
#     params 包含如下属性
#         from,to,payload,app_key
#     '''
#     sn = uuid.uuid4().hex
#     payload = params['payload'] 
#     packet = {
#         'envelope':{
#             'id':sn,
#             'type':1,
#             'ack':1,
#             'from':params['from'],
#             'to':params['to'],
#         },        
#         'payload':payload,
#         'vsn':'0.0.1'
#     }
#     logger.debug(packet)
#     host,port = settings.emsg_inf_push_host,settings.emsg_inf_push_port 
#     transport = TSocket.TSocket(host , port)
#     transport = TTransport.TBufferedTransport(transport)
#     protocol = TBinaryProtocol.TBinaryProtocol(transport)
#     client = emsg_inf_push.Client(protocol)
#     transport.open()
#     client.process(params['app_key'],sn,json.dumps(packet) )
#     transport.close()
#     return success(True)
