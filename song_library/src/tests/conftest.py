import pytest
import pytest_asyncio
from starlette.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.models import Song

from app.main import app


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client
    

@pytest_asyncio.fixture(scope='function')
async def mongo_mock(monkeypatch):
    mongo_client = AsyncMongoMockClient()
    db = mongo_client['karaoke']
    song_library = db['song-library']

    song_get_1: Song = {
        '_id': '643783a9116920ccf2d56529',
        'song_title': 'song title GET 1',
        'artist': 'artist GET 1'
    }
    await song_library.insert_one(song_get_1)

    song_get_2: Song = {
        '_id': '64382e17116920ccf2d5652a',
        'song_title': 'song title GET 2',
        'artist': 'artist GET 2'
    }
    await song_library.insert_one(song_get_2)

    song_update: Song = {
        '_id': '64382e2f116920ccf2d5652c',
        'song_title': 'song title UPDATE',
        'artist': 'artist UPDATE'
    }
    await song_library.insert_one(song_update)

    song_delete: Song = {
        '_id': '648d2e5202df417c254e4795',
        'song_title': 'song title DELETE',
        'artist': 'artist DELETE'
    }
    await song_library.insert_one(song_delete)

    def mock_db():
        return db 
    
    monkeypatch.setattr('app.db.get_db', mock_db)