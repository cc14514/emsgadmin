# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class EmsgDomain(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    userid = models.CharField(max_length=64L, blank=True)
    name = models.CharField(max_length=300L)
    description = models.CharField(max_length=500L, blank=True)
    class Meta:
        db_table = 'emsg_domain'

class EmsgDomainConfig(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    domain = models.CharField(max_length=300L)
    attr = models.CharField(max_length=50L)
    value = models.CharField(max_length=300L, blank=True)
    class Meta:
        db_table = 'emsg_domain_config'

class EmsgOfflineConfig(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    domain = models.CharField(max_length=300L, blank=True)
    attr = models.CharField(max_length=50L, blank=True)
    value = models.CharField(max_length=300L, blank=True)
    class Meta:
        db_table = 'emsg_offline_config'

class EmsgStatErlang(models.Model):
    id = models.CharField(max_length=32L, primary_key=True)
    sys_mem = models.IntegerField()
    process_mem = models.IntegerField()
    session_proc = models.IntegerField()
    http_proc = models.IntegerField(null=True, blank=True)
    redis_handler_proc = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'emsg_stat_erlang'

class EmsgStatRedis(models.Model):
    id = models.CharField(max_length=32L, primary_key=True)
    cpu = models.IntegerField(null=True, blank=True)
    memory_used = models.IntegerField()
    memory_peak = models.IntegerField()
    ops_per_second = models.IntegerField()
    client_connected = models.IntegerField()
    client_blocked = models.IntegerField()
    class Meta:
        db_table = 'emsg_stat_redis'

class EmsgStatSessionDaily(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    domain = models.CharField(max_length=300L)
    total_count = models.IntegerField()
    time = models.CharField(max_length=32L)
    class Meta:
        db_table = 'emsg_stat_session_daily'

class EmsgStatSessionHourly(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    domain = models.CharField(max_length=300L)
    total_count = models.IntegerField()
    time = models.CharField(max_length=32L)
    class Meta:
        db_table = 'emsg_stat_session_hourly'

class EmsgStatSessionSample(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    domain = models.CharField(max_length=300L)
    total_count = models.IntegerField()
    time = models.DateTimeField()
    class Meta:
        db_table = 'emsg_stat_session_sample'

class EmsgSysConfig(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    attr = models.CharField(max_length=50L, blank=True)
    value = models.CharField(max_length=300L, blank=True)
    class Meta:
        db_table = 'emsg_sys_config'

class EmsgUser(models.Model):
    id = models.CharField(max_length=64L, primary_key=True)
    account = models.CharField(max_length=64L, unique=True)
    password = models.CharField(max_length=64L)
    telephone = models.CharField(max_length=64L, blank=True)
    email = models.CharField(max_length=128L, blank=True)
    class Meta:
        db_table = 'emsg_user'

