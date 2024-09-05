import os
from pynamodb.models import Model 
from pynamodb.attributes import (
    UnicodeAttribute, 
    UTCDateTimeAttribute, 
    NumberAttribute
)


AWS_REGION = os.environ['AWS_REGION']
QUEUES_TABLE_NAME = os.environ['QUEUES_TABLE_NAME']
ENQUEUED_SINGERS_TABLE_NAME = os.environ['ENQUEUED_SINGERS_TABLE_NAME']
SONG_CHOICES_TABLE_NAME = os.environ['SONG_CHOICES_TABLE_NAME']


class QueueDB(Model):
    class Meta:
        table_name = QUEUES_TABLE_NAME
        region = AWS_REGION

    queue_id = UnicodeAttribute(hash_key=True)
    location_id = UnicodeAttribute()
    event_date = UTCDateTimeAttribute()
    current_singer_index = NumberAttribute(default=0)


class EnqueuedSingerDB(Model):
    class Meta:
        table_name = ENQUEUED_SINGERS_TABLE_NAME
        region = AWS_REGION

    queue_id = UnicodeAttribute(hash_key=True)
    singer_id = UnicodeAttribute()
    # enqueued_singer_id = UnicodeAttribute()
    queue_position = NumberAttribute(range_key=True)


# class SongChoiceDB(Model):
#     class Meta:
#         table_name = SONG_CHOICES_TABLE_NAME
#         region = AWS_REGION

#     enqueued_singer_id = UnicodeAttribute(hash_key=True)
#     song_id = UnicodeAttribute()
#     position = NumberAttribute(range_key=True)

    