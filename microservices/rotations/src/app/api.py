import uuid
from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .domain import Queue, QueueCreate, EnqueuedSinger, EnqueuedSingerCreate
from .rotations import Rotations


router = APIRouter()


@router.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')


@router.post('/queues/', response_description='Start a queue', response_model=Queue)
def create_queue(queue_data: QueueCreate=Body(...)):
    queue = Rotations.new(queue_data).queue 

    return JSONResponse(status_code=201, content=jsonable_encoder(queue))


@router.get('/queues/{queue_id}', response_description='Get a queue by id', response_model=Queue)
def get_queue(queue_id):
    queue = Rotations.from_db(queue_id).queue
    if queue is not None:
        return JSONResponse(status_code=200, content=jsonable_encoder(queue))
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Queue with id {queue_id} not found.')


@router.post('/queues/{queue_id}/singers/', 
             response_description='Add singer to queue', response_model=Queue)
def enqueue_singer(queue_id, singer_data: EnqueuedSingerCreate=Body(...)):
    rotations = Rotations.from_db(queue_id)
    rotations.add_singer(singer_data.singer_id)

    return JSONResponse(status_code=201, content=jsonable_encoder(rotations.queue))


@router.get('/queues/{queue_id}/singers/{position_id}')
def get_singer(queue_id, position_id):
    pass


@router.delete('/queues/{queue_id}/singers/{enqueued_singer_id}',
               response_description='Remove singer from queue', response_model=Queue)
def remove_singer(queue_id, singer_id):
    pass 
