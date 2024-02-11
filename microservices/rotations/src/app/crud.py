from datetime import datetime
import uuid
from .models import QueueDB, EnqueuedSingerDB, SongChoiceDB
from .domain import QueueCreate, Queue, EnqueuedSinger


def create_song_choice(enqueued_singer_id: uuid.UUID, 
                       song_id: str, 
                       position: int):

    song_choice = SongChoiceDB(enqueued_singer_id=str(enqueued_singer_id), 
                             song_id=song_id, 
                             position=position)
    
    return song_choice.save()


def get_song_choices(enqueued_singer_id: uuid.UUID):
    return SongChoiceDB.query(enqueued_singer_id)


def update_song_choices(choices: list[SongChoiceDB]):    
    for choice in choices:
        choice.save()


def create_enqueued_singer(queue_id: uuid.UUID, 
                           singer_id: uuid.UUID, 
                           enqueued_singer_id: uuid.UUID, 
                           queue_position: int):
        
    enqueued_singer_db = EnqueuedSingerDB(queue_id=str(queue_id), 
                                     singer_id=str(singer_id), 
                                     enqueued_singer_id=str(enqueued_singer_id), 
                                     queue_position=queue_position)
    
    enqueued_singer_db.save()
    
    return EnqueuedSinger(singer_id=enqueued_singer_db.singer_id,
                          enqueued_singer_id=enqueued_singer_db.enqueued_singer_id,
                          position=enqueued_singer_db.queue_position)


def get_enqueued_singers(queue_id: uuid.UUID):
    return EnqueuedSingerDB.query(queue_id)


def update_enqueued_singers(singers: list[EnqueuedSingerDB]):
    for singer in singers:
        singer.save()

def delete_enqueued_singer(queue_id: uuid.UUID, position: int):
    singer = EnqueuedSingerDB(str(queue_id), position)
    singer.delete()

def create_queue(queue_data: QueueCreate):
    queueDB = QueueDB(queue_id=str(uuid.uuid4()), 
                  location_id=str(queue_data.location_id), 
                  event_date=datetime.now())
    queueDB.save()

    return Queue(queue_id=queueDB.queue_id, 
                 location_id=queueDB.location_id, 
                 event_date=queueDB.event_date,
                 current_singer_index=queueDB.current_singer_index)


def get_queue(queue_id):
    queueDB = QueueDB.get(queue_id)

    return Queue(queue_id=queueDB.queue_id,
                 location_id=queueDB.location_id,
                 event_date=queueDB.event_date,
                 current_singer_index=queueDB.current_singer_index)
