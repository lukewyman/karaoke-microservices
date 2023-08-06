import uuid 
from datetime import datetime
from moto import mock_dynamodb
from app.models import Queue, EnqueuedSinger, SongChoice
import app.crud as crud
from .data import SONG_CHOICES, ENQUEUED_SINGERS


def _setup_queues_table():
    Queue.create_table()


def _setup_enqueued_singers_table():
    EnqueuedSinger.create_table()


def _populate_enqueued_singers_table(enqueued_singers):
    for enqueued_singer in enqueued_singers:
        EnqueuedSinger(**enqueued_singer).save()


def _setup_song_choices_table():
    SongChoice.create_table()

def _populate_song_choices_table(choices):
    for choice in choices:
        SongChoice(**choice).save()


@mock_dynamodb
def test_create_song_choice():
    _setup_song_choices_table()

    enqueued_singer_id = uuid.uuid4()
    song_id = 'song-1'
    position_id = 1

    crud.create_song_choice(enqueued_singer_id=enqueued_singer_id, 
                            song_id=song_id, 
                            position=position_id)

    assert SongChoice.count() == 1


@mock_dynamodb
def test_get_song_choices():
    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    enqueued_singer_id = 'e2520391-b24c-41ca-96c0-1e8813272d85'
    choices = list(crud._get_song_choices(enqueued_singer_id=enqueued_singer_id))

    assert len(choices) == 3


@mock_dynamodb
def test_update_song_choices():
    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    enqueued_singer_id = 'e2520391-b24c-41ca-96c0-1e8813272d85'
    choices = list(crud._get_song_choices(enqueued_singer_id=enqueued_singer_id))

    # Change song choice positions
    assert choices[0].song_id == 'song-choice-1'
    choices[0].position = 3
    assert choices[1].song_id == 'song-choice-2'
    choices[1].position = 1
    assert choices[2].song_id == 'song-choice-3'
    choices[2].position = 2

    crud._update_song_choices(choices=choices)

    updated_choices = list(crud._get_song_choices(enqueued_singer_id=enqueued_singer_id))

    assert len(updated_choices) == 3
    assert updated_choices[0].song_id == 'song-choice-2'
    assert updated_choices[0].position == 1
    assert updated_choices[1].song_id == 'song-choice-3'
    assert updated_choices[1].position == 2
    assert updated_choices[2].song_id == 'song-choice-1'
    assert updated_choices[2].position == 3


@mock_dynamodb
def test_update_choices_with_new_choice():

    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    enqueued_singer_id = 'e2520391-b24c-41ca-96c0-1e8813272d85'
    choices = list(crud._get_song_choices(enqueued_singer_id=enqueued_singer_id))
    new_choice = SongChoice(enqueued_singer_id=enqueued_singer_id, 
                            song_id='song-choice-4', 
                            position=4)
    choices.append(new_choice)

    crud._update_song_choices(choices)

    updated_choices = list(crud._get_song_choices(enqueued_singer_id=enqueued_singer_id))

    assert len(updated_choices) == 4


@mock_dynamodb
def test_create_enqueued_singer():
    _setup_enqueued_singers_table()

    queue_id = uuid.uuid4()
    singer_id = uuid.uuid4()
    enqueued_singer_id = uuid.uuid4()
    queue_position = 1

    crud.create_enqueued_singer(queue_id=queue_id, 
                                singer_id=singer_id, 
                                enqueued_singer_id=enqueued_singer_id, 
                                queue_position=queue_position)
    
    assert EnqueuedSinger.count() == 1


@mock_dynamodb
def test_get_enqueued_singers():
    _setup_enqueued_singers_table()
    _populate_enqueued_singers_table(ENQUEUED_SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    enqueued_singers = list(crud._get_enqueued_singers(queue_id))

    assert len(enqueued_singers) == 3


@mock_dynamodb
def test_update_enqueued_singers():
    _setup_enqueued_singers_table()
    _populate_enqueued_singers_table(ENQUEUED_SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    enqueued_singers = list(crud._get_enqueued_singers(queue_id))

    # Change singer positions
    assert enqueued_singers[0].enqueued_singer_id == 'c61b078e-4046-4ea8-bf6b-8620cf040703'
    enqueued_singers[0].queue_position = 3
    assert enqueued_singers[1].enqueued_singer_id == '5776f6f7-3a51-4dd4-b21c-31625887ac7f'
    enqueued_singers[1].queue_position = 1
    assert enqueued_singers[2].enqueued_singer_id == '48cc41c0-cfe5-4c0b-bf13-6663d4fe99fa'
    enqueued_singers[2].queue_position = 2

    crud._update_enqueued_singers(enqueued_singers)

    updated_singers = list(crud._get_enqueued_singers(queue_id))

    assert updated_singers[0].enqueued_singer_id == '5776f6f7-3a51-4dd4-b21c-31625887ac7f'
    assert updated_singers[0].queue_position == 1
    assert updated_singers[1].enqueued_singer_id == '48cc41c0-cfe5-4c0b-bf13-6663d4fe99fa'
    assert updated_singers[1].queue_position == 2
    assert updated_singers[2].enqueued_singer_id == 'c61b078e-4046-4ea8-bf6b-8620cf040703'
    assert updated_singers[2].queue_position == 3


@mock_dynamodb
def test_update_enqueued_singers_with_new_singer():
    _setup_enqueued_singers_table()
    _populate_enqueued_singers_table(ENQUEUED_SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    enqueued_singers = list(crud._get_enqueued_singers(queue_id))

    new_singer = EnqueuedSinger(queue_id=queue_id,
                                singer_id='8d8dcd6c-44bf-4fce-8d1c-c0d102798c35',
                                enqueued_singer_id='d28160fc-4db8-4671-a33a-a64561d3c074',
                                queue_position=4)
    enqueued_singers.append(new_singer)
    crud._update_enqueued_singers(enqueued_singers)
    updated_singers = list(crud._get_enqueued_singers(queue_id))

    assert len(updated_singers) == 4

@mock_dynamodb
def test_create_queue():
    _setup_queues_table() 

    location_id = uuid.uuid4()
    crud.create_queue(location_id=location_id)

    assert Queue.count() == 1
