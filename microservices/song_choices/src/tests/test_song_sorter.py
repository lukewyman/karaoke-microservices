from app.domain import SongChoice
import app.song_sorter as song_sorter
from uuid import uuid4


def test_add_song_to_empty_list():
    empty_choices = []
    queue_id = uuid4()
    singer_id = uuid4()
    song_id = 'new song'

    new_choice = song_sorter.new_song_choice(song_choices=empty_choices, 
                                 queue_id=queue_id, 
                                 singer_id=singer_id,
                                 song_id=song_id)
    
    assert new_choice.queue_id == queue_id
    assert new_choice.singer_id == singer_id
    assert new_choice.song_id == song_id
    assert new_choice.position == 1


def test_add_song_to_existing_list():
    queue_id = uuid4()
    singer_id = uuid4()
    choices = [
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="existing_song_1", position=1),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="existing_song_2", position=2),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="existing_song_3", position=3)
    ]
    
    song_id = 'new_song'
    new_choice = song_sorter.new_song_choice(song_choices=choices, 
                                 queue_id=queue_id, 
                                 singer_id=singer_id,
                                 song_id=song_id)
    
    assert new_choice.queue_id == queue_id
    assert new_choice.singer_id == singer_id
    assert new_choice.song_id == song_id
    assert new_choice.position == 4


def test_next_song_returns_first_song_in_list():
    queue_id = uuid4()
    singer_id = uuid4()
    choices = [
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="existing_song_1", position=1),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="existing_song_2", position=2),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="existing_song_3", position=3)
    ]

    next_choice = song_sorter.next_song_choice(choices)
    
    assert next_choice.song_id == "existing_song_1"
    assert next_choice.position == 1


def test_next_song_from_empty_list_returns_null():
    empty_choices = []

    next_choice = song_sorter.next_song_choice(empty_choices)

    assert next_choice is None


def test_delete_last_song_in_list():
    queue_id = uuid4()
    singer_id = uuid4()
    delete_song_id = "song_3"
    deletion_choice = SongChoice(queue_id=queue_id, singer_id=singer_id, 
                                 song_id=delete_song_id, position=3)
    choices = [
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_1", position=1),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_2", position=2),
        deletion_choice
    ]

    new_choices, deleted_choice = song_sorter.delete_song_choice(song_choices=choices, 
                                                                 song_id=delete_song_id)

    assert len(new_choices) == 2
    assert new_choices[0].song_id == "song_1"
    assert new_choices[0].position == 1
    assert new_choices[1].song_id == "song_2"
    assert new_choices[1].position == 2
    assert deleted_choice == deletion_choice


def test_delete_first_song_in_list():
    queue_id = uuid4()
    singer_id = uuid4()
    delete_song_id = "song_1"
    deletion_choice = SongChoice(queue_id=queue_id, singer_id=singer_id, 
                                 song_id=delete_song_id, position=1)
    choices = [
        deletion_choice,
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_2", position=2),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_3", position=3)
    ]

    new_choices, deleted_choice = song_sorter.delete_song_choice(song_choices=choices, 
                                                                 song_id=delete_song_id)

    assert len(new_choices) == 2
    assert new_choices[0].song_id == "song_2"
    assert new_choices[0].position == 1
    assert new_choices[1].song_id == "song_3"
    assert new_choices[1].position == 2
    assert deleted_choice == deletion_choice


def test_delete_song_in_middle_of_list():
    queue_id = uuid4()
    singer_id = uuid4()
    delete_song_id = "song_3"
    deletion_choice = SongChoice(queue_id=queue_id, singer_id=singer_id, 
                                 song_id=delete_song_id, position=3)
    
    choices = [
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_1", position=1),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_2", position=2),
        deletion_choice,
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_4", position=4),
        SongChoice(queue_id=queue_id, singer_id=singer_id, song_id="song_5", position=5),
    ]

    new_choices, deleted_choice = song_sorter.delete_song_choice(song_choices=choices, 
                                                                 song_id=delete_song_id)
    
    assert len(new_choices) == 4
    assert new_choices[0].song_id == "song_1"
    assert new_choices[0].position == 1
    assert new_choices[1].song_id == "song_2"
    assert new_choices[1].position == 2
    assert new_choices[2].song_id == "song_4"
    assert new_choices[2].position == 3
    assert new_choices[3].song_id == "song_5"
    assert new_choices[3].position == 4
    assert deleted_choice == deletion_choice


def test_move_last_choice_to_the_beginning():
    pass

