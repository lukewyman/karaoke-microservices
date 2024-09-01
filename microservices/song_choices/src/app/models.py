import os
from pynamodb.models import Model 
from pynamodb.attributes import (
    UnicodeAttribute, 
    UTCDateTimeAttribute, 
    NumberAttribute
)


AWS_REGION = os.environ['AWS_REGION']
SONG_CHOICES_TABLE_NAME = os.environ['SONG_CHOICES_TABLE_NAME']

class SongChoiceDB(Model):
    class Meta:
        table_name = SONG_CHOICES_TABLE_NAME
        region = AWS_REGION
    
    enqueued_singer_id = UnicodeAttribute(hash_key=True)
    song_id = UnicodeAttribute()
    position = NumberAttribute(range_key=True)