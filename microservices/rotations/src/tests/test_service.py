import requests
import pytest
import uuid
from app.service import post_song_choice, get_next_song_choice, delete_song_choice, get_singer
from .mock_response import MockResponse


def test_post_song_choice(monkeypatch):

    def mock_post(*args, **kwargs):
        return MockResponse(201, {"queue_id": "test_queue_id",
                                    "singer_id": "test_singer_id",
                                    "song_id": "test_song_id",
                                    "position": 1 
                                })
    
    monkeypatch.setattr(requests, "post", mock_post)

    test_post_song_choice = post_song_choice(queue_id="test_queue_id", 
                                        singer_id="test_singer_id", 
                                        song_id="test_song_id")
    
    assert test_post_song_choice['queue_id'] == "test_queue_id"
    assert test_post_song_choice['singer_id'] == "test_singer_id"
    assert test_post_song_choice['song_id'] == "test_song_id"
    assert test_post_song_choice['position'] == 1


def test_next_song_choice(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(200, {"song_id": "test_song_id",
                                  "song_title": "test_song_title",
                                  "artist": "test_artist"
                            })

    monkeypatch.setattr(requests, "get", mock_get)

    test_next_song_choice = get_next_song_choice(queue_id="test_queue_id", 
                                                 singer_id="test_singer_id")
    
    assert test_next_song_choice['song_id'] == "test_song_id" 
    assert test_next_song_choice['song_title'] == "test_song_title"
    assert test_next_song_choice['artist'] == "test_artist"


def test_next_song_choice_not_found(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(404, {'message': 'Song not found.'})
    
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
        get_next_song_choice(queue_id="test_queue_id", singer_id="test_singer_id")


def test_delete_song_choice(monkeypatch):

    def mock_delete(*args, **kwargs):
        return MockResponse(204, {})
    
    monkeypatch.setattr(requests, "delete", mock_delete)

    delete_song_choice(queue_id=uuid.uuid4(), singer_id=uuid.uuid4(), song_id="test_song_id")


def test_delete_song_choice_not_found(monkeypatch):

    def mock_delete(*args, **kwargs):
        return MockResponse(404, {"Song choice not found"})
    
    monkeypatch.setattr(requests, "delete", mock_delete)

    with pytest.raises(ValueError):
        delete_song_choice(queue_id=uuid.uuid4(), singer_id=uuid.uuid4(), song_id="test_song_id")


def test_get_singer(monkeypatch):

    singer_id = uuid.uuid4()
    def mock_get(*args, **kwargs):
        return MockResponse(200, {"singer_id": str(singer_id),
                                  "email": "test_email",
                                  "first_name": "test_first_name",
                                  "last_name": "test_last_name",
                                  "stage_name": "test_stage_name"})
    
    monkeypatch.setattr(requests, "get", mock_get)

    test_get_singer = get_singer(singer_id=singer_id)

    assert test_get_singer['singer_id'] == str(singer_id)
    assert test_get_singer['email'] == "test_email"
    assert test_get_singer['first_name'] == "test_first_name"
    assert test_get_singer['last_name'] == "test_last_name"
    assert test_get_singer['stage_name'] == "test_stage_name"


def test_get_singer_not_found(monkeypatch):

    singer_id = uuid.uuid4()
    def mock_get(*args, **kwargs):
        return MockResponse(404, 'Singer not found')
    
    monkeypatch.setattr(requests, "get", mock_get) 

    with pytest.raises(ValueError):
        get_singer(singer_id=singer_id)