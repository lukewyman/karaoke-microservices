from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .domain import Queue, QueueCreate, EnqueuedSingerCreate
from . import crud


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')


@router.post('/queues/', response_description='Start a queue', response_model=Queue)
def create_queue(queue_data: QueueCreate=Body(...)):
    queue = crud.create_queue(queue_data=queue_data)

    return JSONResponse(status_code=201, content=jsonable_encoder(queue))


@router.post('/queues/{queue_id}/singers/{enqueued_singer_id}/', 
             response_description='Add singer to queue', response_class=Queue)
def enqueue_singer(singer_data: EnqueuedSingerCreate=Body(...)):
    pass
