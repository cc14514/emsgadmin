import uuid
from session import *


def insertOrUpdateHourly(hourly):
    '''insert if not exist, or update if total_count is bigger'''
    try:
        dbHourly = EmsgStatSessionHourly.get(
            EmsgStatSessionHourly.domain == hourly.domain,
            EmsgStatSessionHourly.time == hourly.time)

        if dbHourly.total_count < hourly.total_count:
            dbHourly.total_count = hourly.total_count
            dbHourly.save()

    except:
        dbHourly = EmsgStatSessionHourly.create(
            id=uuid.uuid1(), domain=hourly.domain,
            time=hourly.time, total_count=hourly.total_count)


def insertOrUpdateDaily(daily):
    '''insert if not exist, or update if total_count is bigger'''
    try:
        dbDaily = EmsgStatSessionDaily.get(
            EmsgStatSessionDaily.domain == daily.domain,
            EmsgStatSessionDaily.time == daily.time)

        if dbDaily.total_count < daily.total_count:
            dbDaily.total_count = daily.total_count
            dbDaily.save()

    except:
        dbDaily = EmsgStatSessionDaily.create(
            id=uuid.uuid1(), domain=daily.domain,
            time=daily.time, total_count=daily.total_count)
