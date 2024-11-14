from datetime import datetime
import uuid
from .models import QueueDB, SingerDB
from .domain import QueueCreate, Queue, Singer
from .mappers import to_singer, to_singer_db


def create_singer(queue_id: uuid.UUID, 
                           singer_id: uuid.UUID, 
                           position: int):
        
    singer_db = SingerDB(queue_id=str(queue_id), 
                                     singer_id=str(singer_id), 
                                     position=position)
    
    singer_db.save()
    
    return Singer(singer_id=singer_db.singer_id,
                          position=singer_db.position)


def get_singers(queue_id: uuid.UUID):
    singer_dbs = SingerDB.query(str(queue_id))
    return [to_singer(singerDB) for singerDB in singer_dbs ]


def update_singers(queue_id: uuid.UUID, singers: list[Singer]):
    for singer in singers:
        singer_db = to_singer_db(queue_id, singer)
        singer_db.save()


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


def update_queue(queue: Queue):
    queue_db = QueueDB(queue_id = queue.queue_id,
                       location_id = queue.location_id,
                       event_date = queue.event_date,
                       current_singer_index = queue.current_singer_index)
    queue_db.save()
