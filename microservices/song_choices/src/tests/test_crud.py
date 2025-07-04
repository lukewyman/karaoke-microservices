import uuid
from moto import mock_dynamodb
from app.models import SongChoiceDB
from app.domain import SongChoice
import app.crud as crud
from .data import (
    SONG_CHOICES,
    _setup_song_choices_table,
    _populate_song_choices_table
)


@mock_dynamodb
def test_create_song_choice():
    _setup_song_choices_table()
    
    queue_id = '1eec4ea6-9ada-42b7-84d6-999dc4727d02'
    singer_id = '523de3ac-6341-45be-bab5-a97981285d1c'
    song_id = 'new_song_choice'
    position = 1

    song_choice = SongChoice(queue_id=queue_id, 
                             singer_id=singer_id, 
                             song_id=song_id, 
                             position=position)
    crud.create_song_choice(song_choice=song_choice)

    assert SongChoiceDB.count() == 1


@mock_dynamodb
def test_get_song_choices():
    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    queue_id = '32e1ce52-f090-46f7-80f1-e998706d3a86'
    singer_id = 'eb571eb2-256c-42b0-a35d-308c169f8b9a'
    choices = crud.get_song_choices(queue_id=queue_id, singer_id=singer_id)

    assert len(choices) == 3
    assert choices[0].queue_id == uuid.UUID('32e1ce52-f090-46f7-80f1-e998706d3a86')
    assert choices[0].singer_id == uuid.UUID('eb571eb2-256c-42b0-a35d-308c169f8b9a')
    assert choices[0].song_id == 'song-choice-1'
    assert choices[0].position == 1
    

@mock_dynamodb
def test_delete_song_choice():
    _setup_song_choices_table()
    
    queue_id = '1eec4ea6-9ada-42b7-84d6-999dc4727d02'
    singer_id = '523de3ac-6341-45be-bab5-a97981285d1c'
    song_id = 'new_song_choice'
    position = 1

    song_choice = SongChoice(queue_id=queue_id, 
                             singer_id=singer_id, 
                             song_id=song_id, 
                             position=position)
    crud.create_song_choice(song_choice=song_choice)

    assert SongChoiceDB.count() == 1

    crud.delete_song_choice(song_choice=song_choice)
    assert SongChoiceDB.count() == 0
