#!/usr/bin/env python
#coding=utf-8

import urllib2, urllib
import json
import datetime
import uuid
import config
from tools import *

now = datetime.datetime.now()
time = now.strftime('%Y-%m-%d %H:%M:%S')
hour = now.strftime('%Y-%m-%d-%H')
date = now.strftime('%Y-%m-%d')

body='{"sn":"' + uuid.uuid1().hex + '","service":"emsg_status","method":"get_total_count","params":{}}'

data = {'body' : body}
f = urllib2.urlopen( url=config.httpconfig['url'], data=urllib.urlencode(data))
response = f.read()

res = json.loads(response)

print json.dumps(res, ensure_ascii=False, indent=4) 
 
entity = res["entity"]["result"]

for data in entity:
		sample = EmsgStatSessionSample.create(
						id=uuid.uuid1(),
						domain=data["domain"],
						time=time,
						total_count=data["total_count"])

		hourly = EmsgStatSessionHourly(
						id=uuid.uuid1(),
                        domain=data["domain"],
                        time=hour,
                        total_count=data["total_count"])

		daily = EmsgStatSessionDaily(
						id=uuid.uuid1(), 
						domain=data["domain"],
						time=date,
						total_count=data["total_count"]) 

		insertOrUpdateHourly(hourly)
		insertOrUpdateDaily(daily)

