from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .db import get_db
from .models import Song


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')

@router.get('/songs/', response_description='Get all Songs', response_model=list[Song])
async def get_all_songs():
    pass

@router.get('/songs/{song_id}', response_description='Get a Song', response_model=Song)
async def get_song(song_id):
    pass