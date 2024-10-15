import requests
import pytest
from app.service import get_song 
from .mock_song import MockSong 
        

def test_get_song(monkeypatch):        
    
    def mock_get(*args, **kwargs):
        return MockSong(200, {"id": "some_id",
                              "song_title": "some song",
                              "artist": "whoever"
                              })
    
    monkeypatch.setattr(requests, "get", mock_get)

    test_song = get_song("some_id")
    assert test_song['id'] == 'some_id'
    assert test_song['song_title'] == 'some song'
    assert test_song['artist'] == 'whoever'


def test_get_song_not_found(monkeypatch):

    def mock_get(*args, **kwargs):
         return MockSong(404, {'message': 'Song not found.'})
    
    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError):
         get_song('some_id')
    