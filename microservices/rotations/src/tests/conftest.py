import uuid
from datetime import datetime
import pytest 
from starlette.testclient import TestClient
from app.domain import Queue, QueueCreate


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

        return None
    

    monkeypatch.setattr('app.rotations.create_enqueued_singer', mock_create_enqueued_singer)