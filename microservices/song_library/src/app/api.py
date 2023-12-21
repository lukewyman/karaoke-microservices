import logging
from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from . import db
from .models import Song, SongData
from .logger import logger


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')


@router.get('/songs', response_description='Get all Songs', response_model=list[Song])
async def get_songs():
    songs = await db.get_all_songs_db()
    return JSONResponse(status_code=200, content=songs)


@router.get('/songs/{song_id}', response_description='Get a Song', response_model=Song)
async def get_song(song_id):
    if (song := await db.get_song_db(song_id)) is not None:
        logger.info(f'Found song with id {song_id} with metadata {song}')
        return JSONResponse(status_code=status.HTTP_200_OK, content=song)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Song with id {song_id} not found.')


@router.post('/songs', response_description='Post a Song', response_model=Song)
async def create_song(song_data: Song=Body(...)):
    song_data = jsonable_encoder(song_data)
    created_song = await db.create_song_db(song_data)
    logger.info(f'Created Song: {created_song}')

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_song)


@router.put('/songs/{song_id}', response_description='Update a Song')
async def update_song(song_id, song_data: SongData=Body(...)):    
    song_data = jsonable_encoder(song_data)
    update_result = await db.update_song_db(song_id, song_data)
    if (update_result.matched_count == 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Song with id {song_id} not found.')

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, 
                        content=f'Song with id {song_id} updated.')


@router.delete('/songs/{song_id}', response_description='Song deleted')
async def delete_song(song_id):
    if (song := await db.get_song_db(song_id)) is not None:
        await db.delete_song_db(song_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=f'Song with id {song_id} deleted.')
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'Song with id {song_id} not found.')
