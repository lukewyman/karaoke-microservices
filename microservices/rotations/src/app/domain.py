import uuid 
from datetime import datetime
from pydantic import BaseModel


class EnqueuedSingerBase(BaseModel):
    singer_id: uuid.UUID


class EnqueuedSingerCreate(EnqueuedSingerBase):
    pass 


class EnqueuedSinger(EnqueuedSingerBase):
    enqueued_singer_id: uuid.UUID
    position: int


class QueueBase(BaseModel):
    location_id: uuid.UUID


class QueueCreate(QueueBase):
    pass 


class Queue(QueueBase):
    queue_id: uuid.UUID
    location_id: uuid.UUID 
    event_date: datetime
    singers: list[EnqueuedSinger] = []
    current_singer_index: int = 0

    class Config:
        orm_mode = True 
        

class Rotations:

    def __init__(self, queue: Queue) -> None:
        self.queue = queue


    @property
    def current_singer(self) -> EnqueuedSinger:
        if len(self.queue.singers) == 0:
            return None
        else:
            return self.queue.singers[self.queue.current_singer_index]
        

    def _get_singer_index(self, singer_id: uuid.UUID):
        for i in range(len(self.queue.singers)):
            if self.queue.singers[i].singer_id == singer_id:
                return i
            
        return -1
    
    
    def add_singer(self, singer_id: uuid.UUID):
        if self._get_singer_index(singer_id) > -1:
            raise ValueError(f'Singer with id {singer_id} already in the queue.')
                
        enqueued_singer = EnqueuedSinger(enqueued_singer_id=uuid.uuid4(),
                                         singer_id=singer_id,
                                         position=1)
        self.queue.singers.append(enqueued_singer)

        return enqueued_singer
    

    def complete_performance(self):
        if self.queue.current_singer_index == len(self.queue.singers) - 1:
            self.queue.current_singer_index = 0
        else:
            self.queue.current_singer_index += 1


    def remove_singer(self, singer_id: uuid.UUID):
        if self._get_singer_index(singer_id) < 0:
            raise ValueError(f'Singer with id {singer_id} is not in the queue.')

        if self._get_singer_index(singer_id) < self.queue.current_singer_index:
            self.queue.current_singer_index -= 1

        if (self._get_singer_index(singer_id) == self.queue.current_singer_index and
            self._get_singer_index(singer_id) == len(self.queue.singers) - 1):
            self.queue.current_singer_index = 0

        self.queue.singers = [s for s in self.queue.singers if s.singer_id != singer_id]


    