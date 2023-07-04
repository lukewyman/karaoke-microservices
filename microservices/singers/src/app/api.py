import logging
import uuid
from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .models import SingerSchema, SingerDB
from . import db


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=status.HTTP_200_OK, content='OK')


@router.post('/singers', response_model=SingerDB, status_code=201)
async def create_singer(data: SingerSchema):
    singer_id = await db.create_singer_db(data=data)
    created_singer = db.get_singer_db(singer_id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_singer)


@router.get('/singers/{singer_id}', response_model=SingerDB)
async def get_singer_by_id(singer_id: uuid.UUID):
    if (singer := await db.get_singer_db(singer_id) is not None):
        return JSONResponse(status_code=status.HTTP_200_OK, content=singer)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Singer with Id {singer_id} not found.')


@router.get('/singers', response_class=list(SingerDB))
async def get_all_singers():
    singers = await db.get_all_singers_db()

    return JSONResponse(status_code=status.HTTP_200_OK, content=singers)


@router.put('/singers/{singer_id}')
async def update_singer(singer_id, data: SingerSchema=(...)):
    await db.update_singer_db(singer_id, data)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/singers/{singer_id}')
async def delete_singer(singer_id):
    await db.delete_singer_db(singer_id)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)