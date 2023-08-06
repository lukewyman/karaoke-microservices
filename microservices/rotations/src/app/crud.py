from datetime import datetime
import uuid
from .models import Queue, EnqueuedSinger, SongChoice


def create_song_choice(enqueued_singer_id: uuid.UUID, 
                       song_id: str, 
                       position: int):

    song_choice = SongChoice(enqueued_singer_id=str(enqueued_singer_id), 
                             song_id=song_id, 
                             position=position)
    
    return song_choice.save()


def _get_song_choices(enqueued_singer_id: uuid.UUID):
    return SongChoice.query(enqueued_singer_id)


def _update_song_choices(choices: list[SongChoice]):    
    for choice in choices:
        choice.save()


def create_enqueued_singer(queue_id: uuid.UUID, 
                           singer_id: uuid.UUID, 
                           enqueued_singer_id: uuid.UUID, 
                           queue_position: int):
        
    enqueued_singer = EnqueuedSinger(queue_id=str(queue_id), 
                                     singer_id=str(singer_id), 
                                     enqueued_singer_id=str(enqueued_singer_id), 
                                     queue_position=queue_position)
    
    return enqueued_singer.save()


def _get_enqueued_singers(queue_id: uuid.UUID):
    return EnqueuedSinger.query(queue_id)


def _update_enqueued_singers(singers: list[EnqueuedSinger]):
    for singer in singers:
        singer.save()


def create_queue(location_id: uuid.UUID):
    queue = Queue(queue_id=str(uuid.uuid4()), 
                  location_id=str(location_id), 
                  event_date=datetime.now())
    
    return queue.save()


def get_queue(queue_id):
    return Queue.get(queue_id)





