import json
import uuid
from starlette.testclient import TestClient
from moto import mock_dynamodb
from app.models import SongChoiceDB
from .data import (
    _setup_song_choices_table,
    _populate_song_choices_table,
    SONG_CHOICES
)


def test_health_check(test_app: TestClient):
    response = test_app.get('/health')
    
    assert response.status_code == 200
    assert response.json() == "OK"


@mock_dynamodb
def test_get_song_choices(test_app: TestClient):
    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
    response = test_app.get(f'/queues/{queue_id}/singers/{singer_id}')

    assert response.status_code == 200
    body = json.loads(response.content)
    assert len(body) == 3
    assert body[0]['queue_id'] == queue_id
    assert body[0]['singer_id'] == singer_id
    assert body[0]['song_id'] == SONG_CHOICES[0]['song_id']
    assert body[0]['position'] == SONG_CHOICES[0]['position']


@mock_dynamodb
def test_get_song_choices_returns_empty_list(test_app: TestClient):
    _setup_song_choices_table()

    queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
    response = test_app.get(f'/queues/{queue_id}/singers/{singer_id}')

    assert response.status_code == 200
    body = json.loads(response.content)
    assert len(body) == 0


@mock_dynamodb
def test_add_song_choice(test_app: TestClient):
    _setup_song_choices_table()

    queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
    song_choice_data = {
        'song_id': SONG_CHOICES[0]['song_id']
    }
    response = test_app.post(f'/queues/{queue_id}/singers/{singer_id}', content=json.dumps(song_choice_data))

    assert response.status_code == 201
    body = json.loads(response.content)
    assert SongChoiceDB.count() == 1


@mock_dynamodb
def test_get_next_choice(test_app: TestClient):
    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
    response = test_app.get(f'/queues/{queue_id}/singers/{singer_id}/songs/next')

    assert response.status_code == 200
    body = json.loads(response.content)
    assert body['song_id'] == SONG_CHOICES[0]['song_id']
    assert body['position'] == 1
    

@mock_dynamodb
def test_get_next_choice_returns_404_not_found_for_empty_choices(test_app: TestClient):
    _setup_song_choices_table()

    queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
    response = test_app.get(f'/queues/{queue_id}/singers/{singer_id}/songs/next')

    assert response.status_code == 404


@mock_dynamodb
def test_delete_song(test_app: TestClient):
    _setup_song_choices_table()
    _populate_song_choices_table(SONG_CHOICES)

    queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
    song_id = SONG_CHOICES[0]['song_id']
    response = test_app.delete(f'/queues/{queue_id}/singers/{singer_id}/songs/{song_id}')

    assert response.status_code == 204
 

# @mock_dynamodb
# def test_delete_song_returns_404_not_found(test_app: TestClient):
#     _setup_song_choices_table()

#     queue_id, singer_id = SONG_CHOICES[0]['enqueued_singer_id'].split(':')
#     song_id = SONG_CHOICES[0]['song_id']
#     response = test_app.delete(f'/queues/{queue_id}/singers/{singer_id}/songs/{song_id}')

#     assert response.status_code == 404