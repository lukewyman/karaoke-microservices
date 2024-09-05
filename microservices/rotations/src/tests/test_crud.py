import uuid 
from datetime import datetime
from moto import mock_dynamodb
from app.models import QueueDB, EnqueuedSingerDB
from app.domain import QueueCreate
import app.crud as crud
from .data import (
    ENQUEUED_SINGERS,
    _setup_queues_table,
    _setup_enqueued_singers_table,
    _populate_enqueued_singers_table
)


@mock_dynamodb
def test_create_enqueued_singer():
    _setup_enqueued_singers_table()

    queue_id = uuid.uuid4()
    singer_id = uuid.uuid4()
    queue_position = 1

    crud.create_enqueued_singer(queue_id=queue_id, 
                                singer_id=singer_id, 
                                queue_position=queue_position)
    
    assert EnqueuedSingerDB.count() == 1


@mock_dynamodb
def test_get_enqueued_singers():
    _setup_enqueued_singers_table()
    _populate_enqueued_singers_table(ENQUEUED_SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    enqueued_singers = list(crud.get_enqueued_singers(queue_id))

    assert len(enqueued_singers) == 3


@mock_dynamodb
def test_update_enqueued_singers():
    _setup_enqueued_singers_table()
    _populate_enqueued_singers_table(ENQUEUED_SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    enqueued_singers = list(crud.get_enqueued_singers(queue_id))

    # Change singer positions
    assert enqueued_singers[0].singer_id == '69400125-d093-41c1-9415-6af0168078f4'
    enqueued_singers[0].queue_position = 3
    assert enqueued_singers[1].singer_id == '110974f0-9185-47c4-ae1b-f890048ea44d'
    enqueued_singers[1].queue_position = 1
    assert enqueued_singers[2].singer_id == 'cf298018-4c0b-4aa9-b8d4-15ea48996811'
    enqueued_singers[2].queue_position = 2

    crud.update_enqueued_singers(enqueued_singers)

    updated_singers = list(crud.get_enqueued_singers(queue_id))

    assert updated_singers[0].singer_id == '110974f0-9185-47c4-ae1b-f890048ea44d'
    assert updated_singers[0].queue_position == 1
    assert updated_singers[1].singer_id == 'cf298018-4c0b-4aa9-b8d4-15ea48996811'
    assert updated_singers[1].queue_position == 2
    assert updated_singers[2].singer_id == '69400125-d093-41c1-9415-6af0168078f4'
    assert updated_singers[2].queue_position == 3


@mock_dynamodb
def test_update_enqueued_singers_with_new_singer():
    _setup_enqueued_singers_table()
    _populate_enqueued_singers_table(ENQUEUED_SINGERS)

    queue_id = '240722c4-16a4-46e5-89fd-773445d7d38e'
    enqueued_singers = list(crud.get_enqueued_singers(queue_id))

    new_singer = EnqueuedSingerDB(queue_id=queue_id,
                                singer_id='8d8dcd6c-44bf-4fce-8d1c-c0d102798c35',
                                queue_position=4)
    enqueued_singers.append(new_singer)
    crud.update_enqueued_singers(enqueued_singers)
    updated_singers = list(crud.get_enqueued_singers(queue_id))

    assert len(updated_singers) == 4


@mock_dynamodb
def test_create_queue():
    _setup_queues_table() 

    queue_data = QueueCreate(location_id=uuid.uuid4())
    queue = crud.create_queue(queue_data)

    assert QueueDB.count() == 1
    