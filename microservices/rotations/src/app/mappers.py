from .domain import Singer, Queue
from .models import SingerDB, QueueDB
import uuid


def to_singer(enqueued_singer_db: SingerDB):
    return Singer(singer_id=enqueued_singer_db.singer_id,
                          position=enqueued_singer_db.queue_position)


def to_singers(enqueued_singer_dbs: list[SingerDB]):
    return [to_singer(es) for es in enqueued_singer_dbs]


def to_singer_db(queue_id: uuid.UUID, enqueued_singer: Singer):
    return SingerDB(str(queue_id), 
                            enqueued_singer.position, 
                            singer_id=str(enqueued_singer.singer_id))


def to_singer_dbs(queue_id: uuid.UUID, singers: Singer):
    return [to_singer_db(queue_id, es) for es in singers]


def to_queue_db(queue: Queue):
    return QueueDB(str(queue.queue_id),
                   location_id = str(queue.location_id),
                   event_date = queue.event_date,
                   current_singer_index = queue.current_singer_index)