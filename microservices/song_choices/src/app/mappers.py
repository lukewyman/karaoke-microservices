from .domain import SongChoice
from .models import SongChoiceDB


def to_song_choice(song_choice_db: SongChoiceDB):
    queue_id, singer_id = song_choice_db.enqueued_singer_id.split(':')

    return SongChoice(queue_id=queue_id,
                      singer_id=singer_id,
                      song_id=song_choice_db.song_id,
                      position=song_choice_db.position)


def to_song_choice_db(song_choice: SongChoice):
    enqueued_singer_id = ':'.join([str(song_choice.queue_id), str(song_choice.singer_id)])

    return SongChoiceDB(enqueued_singer_id=enqueued_singer_id,
                        song_id=song_choice.song_id,
                        position=song_choice.position)