import uuid
from datetime import datetime
import pytest 
from dotenv import load_dotenv
from starlette.testclient import TestClient
from app.domain import Queue, QueueCreate, EnqueuedSinger


load_dotenv(".test.env")

from app.main import app


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='function')
def mock_crud(monkeypatch):

    def mock_create_enqueued_singer(queue_id: uuid.UUID, 
                           singer_id: uuid.UUID, 
                           enqueued_singer_id: uuid.UUID, 
                           queue_position: int):

        return EnqueuedSinger(singer_id=singer_id,
                              enqueued_singer_id=enqueued_singer_id,
                              position=queue_position)
    
    
    def mock_create_queue(queue_data: QueueCreate):
        return None
    

    monkeypatch.setattr('app.rotations.create_queue', mock_create_queue)
    monkeypatch.setattr('app.rotations.create_enqueued_singer', mock_create_enqueued_singer)