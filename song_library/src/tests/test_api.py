import json
import bson 
from . import db_data

def test_health_check(test_app):
    response = test_app.get('/health')
    
    assert response.status_code == 200
    assert response.json() == "OK"


def test_GET_songs(test_app, mongo_mock):
    response = test_app.get('/songs')

    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_GET_song_by_id(test_app, mongo_mock):
    song_id = db_data.API_song_GET['_id']
    response = test_app.get(f'/songs/{song_id}')

    assert response.status_code == 200
    assert response.json() == db_data.API_song_GET


def test_GET_song_not_found(test_app, mongo_mock):
    bad_song_id = '648d4b86846cc6d6d8776087'
    response = test_app.get(f'/songs/{bad_song_id}')

    assert response.status_code == 404


def test_POST_song(test_app, mongo_mock):
    response = test_app.post('/songs', content=json.dumps(db_data.API_song_POST))
    
    assert response.status_code == 201
    song = response.json()
    assert '_id' in song 
    assert bson.objectid.ObjectId.is_valid(song['_id'])
    assert song['song_title'] == db_data.API_song_POST['song_title']
    assert song['artist'] == db_data.API_song_POST['artist']

def test_PUT_song(test_app, mongo_mock):
    song_id = db_data.API_song_PUT['_id']
    song_update = {
        'song_title': 'API song title PUT changed',
        'artist': 'API artist PUT changed'
    }
    response = test_app.put(f'/songs/{song_id}', content=json.dumps(song_update))

    assert response.status_code == 204


def test_PUT_song_not_found(test_app, mongo_mock):
    bad_song_id = '648e01cc715727fa837ea85e'
    song_update = {
        'song_title': 'API song title PUT changed',
        'artist': 'API artist PUT changed'
    }
    response = test_app.put(f'/songs/{bad_song_id}', content=json.dumps(song_update))

    assert response.status_code == 404


def test_DELETE_song(test_app, mongo_mock):
    song_id = db_data.API_song_DELETE['_id']
    delete_response = test_app.delete(f'/songs/{song_id}')

    assert delete_response.status_code == 204

    get_response = test_app.get(f'/songs/{song_id}')

    assert get_response.status_code == 404


def test_DELETE_song_not_found(test_app, mongo_mock):
    bad_song_id = '648e01cc715727fa837ea85e'
    delete_response = test_app.delete(f'/songs/{bad_song_id}')

    assert delete_response.status_code == 404