import uuid 
from datetime import datetime
from app.domain import Queue
from app.rotations import Rotations
import pytest


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


def test_create_an_empty_queue(rotations_fixture):    
    assert len(rotations_fixture.queue.singers) == 0
    assert rotations_fixture.current_singer == None


def test_add_a_singer_to_a_queue(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])

    assert len(rotations_fixture.queue.singers) == 1
    assert rotations_fixture.current_singer.singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[0].position == 1


def test_add_multiple_singers_to_a_queue(rotations_fixture, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])
    
    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[0].position == 1
    assert rotations_fixture.queue.singers[1].position == 2
    assert rotations_fixture.queue.singers[2].position == 3


def test_cannot_add_singer_already_in_rotation(rotations_fixture, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])

    with pytest.raises(ValueError):
        rotations_fixture.add_singer(singers_fixture[2])


def test_completing_performance_advances_queue_to_next_singer(rotations_fixture, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])

    rotations_fixture.complete_performance()

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[2]


def test_completing_performance_twice_advances_queue_2_singers(rotations_fixture, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])

    rotations_fixture.complete_performance()
    rotations_fixture.complete_performance()

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[3]


def test_completing_performance_for_last_singer_returns_to_beginning_of_rotation(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])

    #advance to last singer
    rotations_fixture.complete_performance()
    rotations_fixture.complete_performance()

    #advance back to first singer
    rotations_fixture.complete_performance()

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[1]


def test_rotation_in_correct_state_after_removing_singer_after_current(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])
    rotations_fixture.add_singer(singers_fixture[4])

    #advance to second singer
    rotations_fixture.complete_performance()

    rotations_fixture.remove_singer(singers_fixture[3])

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[2]
    assert rotations_fixture.queue.singers[0].singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[1].singer_id == singers_fixture[2]
    assert rotations_fixture.queue.singers[2].singer_id == singers_fixture[4]


def test_rotation_in_correct_state_after_removing_singer_before_current(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])
    rotations_fixture.add_singer(singers_fixture[4])

    #advance to third singer
    rotations_fixture.complete_performance()
    rotations_fixture.complete_performance()

    rotations_fixture.remove_singer(singers_fixture[2])

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[3]
    assert rotations_fixture.queue.singers[0].singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[1].singer_id == singers_fixture[3]
    assert rotations_fixture.queue.singers[2].singer_id == singers_fixture[4]


def test_rotation_in_correct_state_after_removing_current_singer(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])
    rotations_fixture.add_singer(singers_fixture[4])

    #advance to second singer
    rotations_fixture.complete_performance()

    rotations_fixture.remove_singer(singers_fixture[2])

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[3]
    assert rotations_fixture.queue.singers[0].singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[1].singer_id == singers_fixture[3]
    assert rotations_fixture.queue.singers[2].singer_id == singers_fixture[4]


def test_rotation_in_correct_state_after_removing_current_and_last_singer(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])
    rotations_fixture.add_singer(singers_fixture[3])
    rotations_fixture.add_singer(singers_fixture[4])

    #advance to last singer
    rotations_fixture.complete_performance()
    rotations_fixture.complete_performance()
    rotations_fixture.complete_performance()

    rotations_fixture.remove_singer(singers_fixture[4])

    assert len(rotations_fixture.queue.singers) == 3
    assert rotations_fixture.current_singer.singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[0].singer_id == singers_fixture[1]
    assert rotations_fixture.queue.singers[1].singer_id == singers_fixture[2]
    assert rotations_fixture.queue.singers[2].singer_id == singers_fixture[3]


def test_cannot_remove_singer_that_is_not_in_rotation(rotations_fixture: Rotations, singers_fixture, mock_crud):
    rotations_fixture.add_singer(singers_fixture[1])
    rotations_fixture.add_singer(singers_fixture[2])

    with pytest.raises(ValueError):
        rotations_fixture.remove_singer(singers_fixture[3])