import pytest
import bson
from app.db import create_song
from app.db import delete_song
from app.db import get_all_songs
from app.db import get_song 
from app.db import update_song
from app.models import Song 

@pytest.mark.asyncio
async def test_get_all_songs(mongo_mock):
    songs = await get_all_songs()

    assert len(songs) >= 2


@pytest.mark.asyncio
async def test_get_song(mongo_mock):
    song = await get_song('643783a9116920ccf2d56529')

    assert song['_id'] == '643783a9116920ccf2d56529'
    assert song['song_title'] == 'song title GET 1'
    assert song['artist'] == 'artist GET 1'


@pytest.mark.asyncio
async def test_create_song(mongo_mock):
    song: dict = {
        'song_title': 'song title CREATE',
        'artist': 'artist CREATE'
    }
    created_song = await create_song(song)
    song_id = created_song.get('_id', None)

    assert bson.objectid.ObjectId.is_valid(song_id)
    assert song['song_title'] == 'song title CREATE'
    assert song['artist'] == 'artist CREATE'


@pytest.mark.asyncio
async def test_update_song(mongo_mock):
    song_update: dict = {
        'song_title': 'UPDATED song title',
        'artist': 'UPDATED artist'
    }
    update_result = await update_song('64382e2f116920ccf2d5652c', song_update)
    
    assert update_result.matched_count == 1
    assert update_result.modified_count == 1


@pytest.mark.asyncio
async def test_delete_song(mongo_mock):
    delete_id = '648d2e5202df417c254e4795'
    delete_result = await delete_song('648d2e5202df417c254e4795')

    assert delete_result.deleted_count == 1
