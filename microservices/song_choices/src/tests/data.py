from app.models import SongChoiceDB
from app.domain import SongChoice


def _setup_song_choices_table():
    SongChoiceDB.create_table()


def _populate_song_choices_table(choices):
    for choice in choices:
        SongChoiceDB(**choice).save()


SONG_CHOICES = [
    {
        'enqueued_singer_id': '32e1ce52-f090-46f7-80f1-e998706d3a86:eb571eb2-256c-42b0-a35d-308c169f8b9a',
        'song_id': 'song-choice-1',
        'position': 1
    },
    {
        'enqueued_singer_id': '32e1ce52-f090-46f7-80f1-e998706d3a86:eb571eb2-256c-42b0-a35d-308c169f8b9a',
        'song_id': 'song-choice-2',
        'position': 2
    },
    {
        'enqueued_singer_id': '32e1ce52-f090-46f7-80f1-e998706d3a86:eb571eb2-256c-42b0-a35d-308c169f8b9a',
        'song_id': 'song-choice-3',
        'position': 3
    }
]