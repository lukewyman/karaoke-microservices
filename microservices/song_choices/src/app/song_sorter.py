from .domain import SongChoice
import uuid 
from typing import List
from typing import Tuple


def _decrement_position(song_choice: SongChoice):
        song_choice.position = song_choice.position - 1
        return song_choice


def _increment_position(song_choice: SongChoice):
        song_choice.position = song_choice.position + 1
        return song_choice


def new_song_choice(song_choices: list[SongChoice], 
                    queue_id: uuid.UUID, 
                    singer_id: uuid.UUID,
                    song_id: str) -> SongChoice:    
    new_position = len(song_choices) + 1
    new_choice = SongChoice(queue_id=queue_id, 
                            singer_id=singer_id, 
                            song_id=song_id, 
                            position=new_position)
    song_choices.append(new_choice)

    return new_choice


def next_song_choice(song_choices: list[SongChoice]) -> SongChoice:

    if len(song_choices) == 0:
        return None

    return song_choices[0]    


def delete_song_choice(song_choices: list[SongChoice], 
                       song_id: str) -> Tuple[List[SongChoice], SongChoice]:    
    
    delete_index = [sc.song_id for sc in song_choices].index(song_id)

    before_choices = song_choices[:delete_index]
    after_choices = song_choices[delete_index+1:]
    after_choices = [_decrement_position(sc) for sc in after_choices]

    return before_choices+after_choices, song_choices[delete_index]


def move_song_choice(song_choices: list[SongChoice],
                     song_id: str,
                     new_position: int) -> List[SongChoice]:    
    pass
    