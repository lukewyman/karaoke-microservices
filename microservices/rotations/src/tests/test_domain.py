import uuid 
from datetime import datetime
from app.domain import Queue, QueueCreate
from app.rotations import Rotations
import pytest
from moto import mock_dynamodb
from .data import (
    SONG_CHOICES, 
    ENQUEUED_SINGERS,
    _setup_queues_table,
    _setup_song_choices_table,
    _setup_enqueued_singers_table,
    _populate_song_choices_table,
    _populate_enqueued_singers_table
)

@pytest.fixture(scope='function')
def rotations_fixture() -> Rotations:
    queue_id = uuid.uuid4()
    location_id = uuid.uuid4()
    event_date = datetime.now()
    return Rotations(Queue(queue_id=queue_id, 
                  location_id=location_id, 
                  event_date=event_date))

@pytest.fixture(scope='module')
def singers_fixture():
    return [
        None,
        uuid.uuid4(),
        uuid.uuid4(),
        uuid.uuid4(),
        uuid.uuid4(),
    ]


@mock_dynamodb
def test_create_an_empty_queue():
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 0
    assert rotations_get.current_singer == None


@mock_dynamodb
def test_add_a_singer_to_a_queue(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    rotations.add_singer(singers_fixture[1])

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 1
    assert rotations_get.current_singer.singer_id == singers_fixture[1]
    assert rotations_get.queue.singers[0].position == 1


@mock_dynamodb
def test_add_multiple_singers_to_a_queue(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))

    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])
    
    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3
    assert rotations_get.current_singer.singer_id == singers_fixture[1]
    assert rotations_get.queue.singers[0].position == 1
    assert rotations_get.queue.singers[1].position == 2
    assert rotations_get.queue.singers[2].position == 3


@mock_dynamodb
def test_cannot_add_singer_already_in_rotation(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))

    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])

    with pytest.raises(ValueError):
        rotations.add_singer(singers_fixture[2])


@mock_dynamodb
def test_completing_performance_advances_queue_to_next_singer(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])

    rotations.complete_performance()

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3
    assert rotations_get.current_singer.singer_id == singers_fixture[2]


@mock_dynamodb
def test_completing_performance_twice_advances_queue_2_singers(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])

    rotations.complete_performance()
    rotations.complete_performance()

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3
    assert rotations_get.current_singer.singer_id == singers_fixture[3]


@mock_dynamodb
def test_completing_performance_for_last_singer_returns_to_beginning_of_rotation(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])

    #advance to last singer
    rotations.complete_performance()
    rotations.complete_performance()

    #advance back to first singer
    rotations.complete_performance()

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3
    assert rotations_get.current_singer.singer_id == singers_fixture[1]


@mock_dynamodb
def test_rotation_in_correct_state_after_removing_singer_after_current(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
        
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])
    rotations.add_singer(singers_fixture[4])

    #advance to second singer
    rotations.complete_performance()

    rotations.remove_singer(singers_fixture[3])

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3, 'Incorrect number of singers after removal.'
    assert rotations_get.current_singer.singer_id == singers_fixture[2], 'Incorrect current singer index.'
    assert rotations_get.queue.singers[0].singer_id == singers_fixture[1], 'Incorrect singer in first position.'
    assert rotations_get.queue.singers[1].singer_id == singers_fixture[2], 'Incorrect singer in second position.'
    assert rotations_get.queue.singers[2].singer_id == singers_fixture[4], 'Incorrect singer in third position.'


@mock_dynamodb
def test_rotation_in_correct_state_after_removing_singer_before_current(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])
    rotations.add_singer(singers_fixture[4])

    #advance to third singer
    rotations.complete_performance()
    rotations.complete_performance()

    rotations.remove_singer(singers_fixture[2])

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3, 'Incorrect number of singers after removal.'
    assert rotations_get.current_singer.singer_id == singers_fixture[3], 'Incorrect current singer index.'
    assert rotations_get.queue.singers[0].singer_id == singers_fixture[1], 'Incorrect singer in first position.'
    assert rotations_get.queue.singers[1].singer_id == singers_fixture[3], 'Incorrect singer in second position.'
    assert rotations_get.queue.singers[2].singer_id == singers_fixture[4], 'Incorrect singer in third position.'


@mock_dynamodb
def test_rotation_in_correct_state_after_removing_current_singer(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])
    rotations.add_singer(singers_fixture[4])

    #advance to second singer
    rotations.complete_performance()

    rotations.remove_singer(singers_fixture[2])

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3
    assert rotations_get.current_singer.singer_id == singers_fixture[3]
    assert rotations_get.queue.singers[0].singer_id == singers_fixture[1]
    assert rotations_get.queue.singers[1].singer_id == singers_fixture[3]
    assert rotations_get.queue.singers[2].singer_id == singers_fixture[4]


@mock_dynamodb
def test_rotation_in_correct_state_after_removing_current_and_last_singer(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))
    
    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])
    rotations.add_singer(singers_fixture[3])
    rotations.add_singer(singers_fixture[4])

    #advance to last singer
    rotations.complete_performance()
    rotations.complete_performance()
    rotations.complete_performance()

    rotations.remove_singer(singers_fixture[4])

    rotations_get = Rotations.from_db(rotations.queue.queue_id)
    assert len(rotations_get.queue.singers) == 3, 'Incorrect number of singers after removal.'
    assert rotations_get.current_singer.singer_id == singers_fixture[1], 'Incorrect current singer index.'
    assert rotations_get.queue.singers[0].singer_id == singers_fixture[1], 'Incorrect singer in first position.'
    assert rotations_get.queue.singers[1].singer_id == singers_fixture[2], 'Incorrect singer in second position.'
    assert rotations_get.queue.singers[2].singer_id == singers_fixture[3], 'Incorrect singer in third position.'


@mock_dynamodb
def test_cannot_remove_singer_that_is_not_in_rotation(singers_fixture):
    _setup_queues_table()
    _setup_enqueued_singers_table()

    location_id = uuid.uuid4()
    rotations = Rotations.new(QueueCreate(location_id=location_id))

    rotations.add_singer(singers_fixture[1])
    rotations.add_singer(singers_fixture[2])

    with pytest.raises(ValueError):
        rotations.remove_singer(singers_fixture[3])