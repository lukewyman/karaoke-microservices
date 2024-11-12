import uuid 
from datetime import datetime
from pydantic import BaseModel


class SingerBase(BaseModel):
    singer_id: uuid.UUID


class SingerCreate(SingerBase):
    pass 


class Singer(SingerBase):
    position: int


class QueueBase(BaseModel):
    location_id: uuid.UUID


class QueueCreate(QueueBase):
    pass 


class Queue(QueueBase):
    queue_id: uuid.UUID
    location_id: uuid.UUID 
    event_date: datetime
    singers: list[Singer] = []
    current_singer_index: int = 0

    class Config:
        orm_mode = True 
