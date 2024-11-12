from datetime import datetime
import uuid
from .models import QueueDB, SingerDB
from .domain import QueueCreate, Queue, Singer


def create_singer(queue_id: uuid.UUID, 
                           singer_id: uuid.UUID, 
                           queue_position: int):
        
    enqueued_singer_db = SingerDB(queue_id=str(queue_id), 
                                     singer_id=str(singer_id), 
                                     queue_position=queue_position)
    
    enqueued_singer_db.save()
    
    return Singer(singer_id=enqueued_singer_db.singer_id,
                          position=enqueued_singer_db.queue_position)


def get_singers(queue_id: uuid.UUID):
    return SingerDB.query(str(queue_id))


def update_singers(singers: list[SingerDB]):
    for singer in singers:
        singer.save()


def delete_singer(queue_id: uuid.UUID, position: int):
    singer = SingerDB(str(queue_id), position)
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
    queueDB = QueueDB.get(str(queue_id))

    return Queue(queue_id=queueDB.queue_id,
                 location_id=queueDB.location_id,
                 event_date=queueDB.event_date,
                 current_singer_index=queueDB.current_singer_index)


def update_queue(queueDB: QueueDB):
    queueDB.save()
