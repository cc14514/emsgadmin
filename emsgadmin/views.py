#!/usr/bin/env python
# coding=utf8
import logging, traceback, json, uuid, collections, urllib, urllib2, datetime, os

from emsgadmin import fileserver_client
from django.http import HttpResponse
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def uploadify(request):
    '''
    图片上传
    '''
    if 'upfile' in request.FILES:
        uf = request.FILES['upfile']
        path = os.path.join('/tmp', uuid.uuid4().hex)
        outputStream = open(path, 'wb+')
        for chunk in uf.chunks():
            outputStream.write(chunk)
        outputStream.close()
        success = fileserver_client.upload(file_path=path)
        entity = success.get('entity')
        if success.get('success'):
            url = fileserver_client.get_file_url(entity.get('id'))
            return HttpResponse(json.dumps({'success': True, 'url': url, 'id': entity.get('id')}))
        else:
            logger.error(success)
    return HttpResponse(json.dumps({'success': False, 'reason': entity.get('reason')}))
