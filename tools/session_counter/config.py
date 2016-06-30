# /usr/bin/env python
# coding=utf8
import logging

# True / False
DEBUG = True

if DEBUG:
    #################################################################
    # 测试
    #################################################################
    logging_cfg = {
        'file': '/tmp/session_counter.log',
        'level': logging.DEBUG
    }

    dbconfig = {
        'host': '192.168.0.214',
        'schema': 'db_emsg',
        'user': 'root',
        'password': '123456'
    }

    httpconfig = {
        'url': 'http://192.168.0.214:4280'
    }

else:
    #################################################################
    # 线上
    #################################################################
    logging_cfg = {
        'file': '/home/appusr/var/log/session_counter.log',
        'level': logging.INFO
    }

    dbconfig = {
        'host': '192.168.2.101',
        'schema': 'db_emsg',
        'user': 'root',
        'password': '123456'
    }

    httpconfig = {
        'url': 'http://192.168.2.101:4280'
    }
