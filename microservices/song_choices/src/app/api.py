import uuid
from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .domain import SongChoiceCreate, SongChoice, SongChoiceUpdate
from . import crud
from . import song_sorter as song_sorter


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')


@router.post('/queues/{queue_id}/singers/{singer_id}', response_model=SongChoice)
def add_song_choice(queue_id, singer_id, song_choice_data: SongChoiceCreate=Body(...)):
    song_choices = crud.get_song_choices(queue_id=queue_id, singer_id=singer_id)
    song_choice = song_sorter.new_song_choice(song_choices=song_choices, 
                                  queue_id=queue_id, 
                                  singer_id=singer_id, 
                                  song_id=song_choice_data.song_id)
    crud.create_song_choice(song_choice)

    return JSONResponse(status_code=201, content=jsonable_encoder(song_choice))


@router.get('/queues/{queue_id}/singers/{singer_id}', response_model=list[SongChoice])
def get_song_choices(queue_id, singer_id):
    song_choices = crud.get_song_choices(queue_id=queue_id, singer_id=singer_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(song_choices))


@router.get('/queues/{queue_id}/singers/{singer_id}/songs/next', response_model=SongChoice)
def get_next_choice(queue_id, singer_id):
    song_choices = crud.get_song_choices(queue_id=queue_id, singer_id=singer_id)
    if len(song_choices) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Next song for queue {queue_id} and singer {singer_id} not found.')

    next = song_sorter.next_song_choice(song_choices=song_choices)
    return JSONResponse(status_code=200, content=jsonable_encoder(next))


@router.delete('/queues/{queue_id}/singers/{singer_id}/songs/{song_id}')
def remove_song_choice(queue_id, singer_id, song_id):
    song_choices = crud.get_song_choices(queue_id=queue_id, singer_id=singer_id)
    song_choices, song_choice = song_sorter.delete_song_choice(song_choices=song_choices, song_id=song_id)
    if song_choice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Song choice for queue {queue_id}, singer {singer_id} and song {song_id} not found.")
    
    crud.delete_song_choice(song_choice=song_choice)
    crud.update_song_choices(song_choices=song_choices)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                        content=f'Song choice with song_id {song_id} deleted.')


@router.put('/queues/{queue_id}/singers/{singer_id}/songs/{song_id}')
def update_song_choice(queue_id, singer_id, song_id, update_data: SongChoiceUpdate=Body(...)):
    pass