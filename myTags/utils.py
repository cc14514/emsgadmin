# /usr/bin/env python
# coding=utf8
'''
Created on 2015年6月24日

@author: liangc
'''


class RequestToken(object):
    tkey = 'request_token'
    disable = 'DISABLE'

    def __init__(self, request):
        self.request = request
        self.session = request.session
        if request.method == 'GET':
            token = request.GET.get(self.tkey)
        elif request.method == 'POST':
            token = request.POST.get(self.tkey)
        if token:
            self.token = token
        else:
            self.token = self.disable
        print 'init requestToken : %s' % self.token

    def set(self, value):
        '''
        设置一个指定的值到session中，key为本次访问的token
        '''
        print 'token=%s ; value=%s' % (self.token, value)
        self.session[self.token] = value

    def fetch(self):
        '''
        当token重复出现时，可以通过此方法取出之前放入token中的值
        '''
        try:
            value = self.session.get(self.token)
        except:
            value = None
        return value

    def check(self):
        '''
        如果这个token曾经出现过，则返回 False,如果 token 为 disable 则直接返回 True，表示不启用此功能
        '''
        try:
            if self.token == self.disable:
                return True
            if self.session.get(self.token):
                return False
        except:
            pass
        return True
