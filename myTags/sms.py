# /usr/bin/env python
# coding=utf8
import datetime
from myTags.poster import *

############################################
## 短信网关配置
############################################

url = "http://www.lx198.com/sdk/send"
sign = "维企网"
username = "cc14514@icloud.com"
pwd = "468F76492018956C975E60E4DC784D4A"



############################################
## 发短信的方法
############################################
curttNo = 0


class SMSSender:
    def send(self, phone, msg):
        form = dict(
            accName=username,
            accPwd=pwd,
            aimcodes=phone,
            content='%s【%s】' % (msg, sign),
            bizId=self._biz_code(),
            dataType="string"
        )
        return submit(url, form)

    def _biz_code(self):
        global curttNo
        if curttNo < 999:
            curttNo = curttNo + 1
        else:
            curttNo = 1
        curttNoStr = '%s' % curttNo
        while len(curttNoStr) < 3:
            curttNoStr = "0%s" % curttNoStr
        return '%s%s' % (datetime.datetime.now().strftime('%y%m%d%H%M%S'), curttNoStr)


sender = SMSSender()


def send(phone, msg):
    return sender.send(phone, msg)
