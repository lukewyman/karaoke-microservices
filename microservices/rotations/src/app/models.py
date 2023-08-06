from pynamodb.models import Model 
from pynamodb.attributes import (
    UnicodeAttribute, 
    UTCDateTimeAttribute, 
    NumberAttribute
)


class Queue(Model):
    class Meta:
        table_name = 'queues'

    queue_id = UnicodeAttribute(hash_key=True)
    location_id = UnicodeAttribute()
    event_date = UTCDateTimeAttribute()


class EnqueuedSinger(Model):
    class Meta:
        table_name = 'enqueued_singers'

    queue_id = UnicodeAttribute(hash_key=True)
    singer_id = UnicodeAttribute()
    enqueued_singer_id = UnicodeAttribute()
    queue_position = NumberAttribute(range_key=True)


class SongChoice(Model):
    class Meta:
        table_name = 'song_choices'

    enqueued_singer_id = UnicodeAttribute(hash_key=True)
    song_id = UnicodeAttribute()
    position = NumberAttribute(range_key=True)

    