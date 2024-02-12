from .domain import EnqueuedSinger, Queue
from .models import EnqueuedSingerDB, QueueDB, SongChoiceDB
import uuid


def to_enqueued_singer(enqueued_singer_db: EnqueuedSingerDB):
    return EnqueuedSinger(singer_id=enqueued_singer_db.singer_id,
                          enqueued_singer_id=enqueued_singer_db.enqueued_singer_id,
                          position=enqueued_singer_db.queue_position)


def to_enqueued_singers(enqueued_singer_dbs: list[EnqueuedSingerDB]):
    return [to_enqueued_singer(es) for es in enqueued_singer_dbs]


def to_enqueued_singer_db(queue_id: uuid.UUID, enqueued_singer: EnqueuedSinger):
    return EnqueuedSingerDB(str(queue_id), 
                            enqueued_singer.position, 
                            enqueued_singer_id=str(enqueued_singer.enqueued_singer_id),
                            singer_id=str(enqueued_singer.singer_id))


def to_enqueued_singer_dbs(queue_id: uuid.UUID, enqueued_singers: EnqueuedSinger):
    return [to_enqueued_singer_db(queue_id, es) for es in enqueued_singers]