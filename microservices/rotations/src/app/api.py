import logging
import uuid 
from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .models import Rotation
from . import db


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')


@router.post('/rotations')
async def create_rotation():
    rotation = Rotation.fromEmpty()
    db.create_rotation_db(rotation)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=rotation)


@router.get('/rotations/{rotation_id}')
async def get_rotation(rotation_id):
    pass


@router.get('/rotations/')
async def get_rotations():
    pass


@router.put('/rotations/{rotation_id}')
async def update_rotation(rotation_id, data: Rotation=Body(...)):
    pass 

@router.delete('/rotations/{rotation_id}')
async def delete_rotation(rotation_id):
    pass