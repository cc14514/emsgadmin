import config
from peewee import *

database = MySQLDatabase(
        config.dbconfig['schema'], 
        **{'host': config.dbconfig['host'], 
            'password': config.dbconfig['password'], 
            'user': config.dbconfig['user']})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class EmsgStatSessionDaily(BaseModel):
    domain = CharField(max_length=300)
    id = CharField(max_length=64, primary_key=True)
    time = CharField(max_length=32)
    total_count = IntegerField()

    class Meta:
        db_table = 'emsg_stat_session_daily'

class EmsgStatSessionHourly(BaseModel):
    domain = CharField(max_length=300)
    id = CharField(max_length=64, primary_key=True)
    time = CharField(max_length=32)
    total_count = IntegerField()

    class Meta:
        db_table = 'emsg_stat_session_hourly'

class EmsgStatSessionSample(BaseModel):
    domain = CharField(max_length=300)
    id = CharField(max_length=64, primary_key=True)
    time = DateTimeField()
    total_count = IntegerField()

    class Meta:
        db_table = 'emsg_stat_session_sample'

