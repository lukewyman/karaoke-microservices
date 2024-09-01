import uuid
from .models import SongChoiceDB
from .domain import SongChoice
from .mappers import to_song_choice, to_song_choice_db


def create_song_choice(song_choice: SongChoice):    
    song_choice_db = to_song_choice_db(song_choice)
        
    return song_choice_db.save()
    

def get_song_choices(queue_id: uuid.UUID, singer_id: uuid.UUID):
    enqueued_singer_id = ':'.join([queue_id, singer_id])

    song_choice_dbs = SongChoiceDB.query(enqueued_singer_id)
    return [to_song_choice(sc) for sc in song_choice_dbs]


def update_song_choices(song_choices: list[SongChoice]):
    for song_choice in song_choices:
        song_choice_db = to_song_choice_db(song_choice)
        song_choice_db.save()


def delete_song_choice(song_choice: SongChoice):
    enqueued_singer_id = ':'.join([str(song_choice.queue_id), str(song_choice.singer_id)])
    song_choice_db = SongChoiceDB(enqueued_singer_id, 
                                  song_choice.song_id, 
                                  song_choice.position)
    
    song_choice_db.delete()