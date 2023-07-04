import pytest
import bson
from app import db
from app.models import Song 
from . import db_data


@pytest.mark.asyncio
async def test_get_all_songs(mongo_mock):
    songs = await db.get_all_songs_db()

    assert len(songs) >= 3


@pytest.mark.asyncio
async def test_get_song_db(mongo_mock):
    song = await db.get_song_db('643783a9116920ccf2d56529')

    assert song == db_data.DB_song_get_1


@pytest.mark.asyncio
async def test_create_song_db(mongo_mock):
    created_song = await db.create_song_db(db_data.DB_song_create)
    song_id = created_song.get('_id', None)

    assert bson.objectid.ObjectId.is_valid(song_id)
    assert created_song['song_title'] == 'song title CREATE'
    assert created_song['artist'] == 'artist CREATE'


@pytest.mark.asyncio
async def test_update_song_db(mongo_mock):
    song_update: dict = {
        'song_title': 'UPDATED song title',
        'artist': 'UPDATED artist'
    }
    update_result = await db.update_song_db('64382e2f116920ccf2d5652c', song_update)
    
    assert update_result.matched_count == 1
    assert update_result.modified_count == 1


@pytest.mark.asyncio
async def test_delete_song_db(mongo_mock):
    delete_id = '648d2e5202df417c254e4795'
    delete_result = await db.delete_song_db(delete_id)

    assert delete_result.deleted_count == 1
