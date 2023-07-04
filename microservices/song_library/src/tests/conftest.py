import pytest
import pytest_asyncio
from starlette.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.models import Song
from . import db_data

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
    
    await song_library.insert_one(db_data.DB_song_get_1)    
    await song_library.insert_one(db_data.DB_song_get_2)    
    await song_library.insert_one(db_data.DB_song_update)    
    await song_library.insert_one(db_data.DB_song_delete)
    await song_library.insert_one(db_data.API_song_GET)
    await song_library.insert_one(db_data.API_song_PUT)
    await song_library.insert_one(db_data.API_song_DELETE)

    def mock_db():
        return db 
    
    monkeypatch.setattr('app.db.get_db', mock_db)