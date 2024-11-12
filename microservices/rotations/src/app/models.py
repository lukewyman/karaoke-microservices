import os
from pynamodb.models import Model 
from pynamodb.attributes import (
    UnicodeAttribute, 
    UTCDateTimeAttribute, 
    NumberAttribute
)


AWS_REGION = os.environ['AWS_REGION']
QUEUES_TABLE_NAME = os.environ['QUEUES_TABLE_NAME']
SINGERS_TABLE_NAME = os.environ['SINGERS_TABLE_NAME']


class QueueDB(Model):
    class Meta:
        table_name = QUEUES_TABLE_NAME
        region = AWS_REGION

    queue_id = UnicodeAttribute(hash_key=True)
    location_id = UnicodeAttribute()
    event_date = UTCDateTimeAttribute()
    current_singer_index = NumberAttribute(default=0)


class SingerDB(Model):
    class Meta:
        table_name = SINGERS_TABLE_NAME
        region = AWS_REGION

    queue_id = UnicodeAttribute(hash_key=True)
    singer_id = UnicodeAttribute()
    queue_position = NumberAttribute(range_key=True)


    