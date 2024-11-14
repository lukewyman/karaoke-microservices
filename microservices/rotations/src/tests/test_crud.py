import uuid 
from datetime import datetime
from moto import mock_dynamodb
from app.models import QueueDB, SingerDB
from app.domain import QueueCreate, Singer
import app.crud as crud
from .data import (
    SINGERS,
    _setup_queues_table,
    _setup_singers_table,
    _populate_singers_table
)


@mock_dynamodb
def test_create_singer():
    _setup_singers_table()

    queue_id = uuid.uuid4()
    singer_id = uuid.uuid4()
    position = 1

    crud.create_singer(queue_id=queue_id, 
                                singer_id=singer_id, 
                                position=position)
    
    assert SingerDB.count() == 1


@mock_dynamodb
def test_get_singers():
    _setup_singers_table()
    _populate_singers_table(SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    singers = list(crud.get_singers(queue_id))

    assert len(singers) == 3


@mock_dynamodb
def test_update_singers():
    _setup_singers_table()
    _populate_singers_table(SINGERS)

    queue_id = uuid.UUID('240722c4-16a4-46e5-89fd-773445d7d38e')
    singers = list(crud.get_singers(queue_id))

    # Change singer positions
    assert singers[0].singer_id == uuid.UUID('69400125-d093-41c1-9415-6af0168078f4')
    singers[0].position = 3
    assert singers[1].singer_id == uuid.UUID('110974f0-9185-47c4-ae1b-f890048ea44d')
    singers[1].position = 1
    assert singers[2].singer_id == uuid.UUID('cf298018-4c0b-4aa9-b8d4-15ea48996811')
    singers[2].position = 2

    crud.update_singers(queue_id, singers)

    updated_singers = list(crud.get_singers(queue_id))

    assert updated_singers[0].singer_id == uuid.UUID('110974f0-9185-47c4-ae1b-f890048ea44d')
    assert updated_singers[0].position == 1
    assert updated_singers[1].singer_id == uuid.UUID('cf298018-4c0b-4aa9-b8d4-15ea48996811')
    assert updated_singers[1].position == 2
    assert updated_singers[2].singer_id == uuid.UUID('69400125-d093-41c1-9415-6af0168078f4')
    assert updated_singers[2].position == 3


@mock_dynamodb
def test_update_singers_with_new_singer():
    _setup_singers_table()
    _populate_singers_table(SINGERS)

    queue_id = uuid.UUID('240722c4-16a4-46e5-89fd-773445d7d38e')
    singers = list(crud.get_singers(queue_id))

    new_singer = Singer(queue_id=queue_id,
                                singer_id='8d8dcd6c-44bf-4fce-8d1c-c0d102798c35',
                                position=4)
    singers.append(new_singer)
    crud.update_singers(queue_id, singers)
    updated_singers = list(crud.get_singers(queue_id))

    assert len(updated_singers) == 4


@mock_dynamodb
def test_create_queue():
    _setup_queues_table() 

    queue_data = QueueCreate(location_id=uuid.uuid4())
    queue = crud.create_queue(queue_data)

    assert QueueDB.count() == 1
    