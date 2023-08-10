import uuid
from .domain import Queue, EnqueuedSinger
from .crud import (
    create_enqueued_singer
)

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
                                         position=len(self.queue.singers) + 1)
        self.queue.singers.append(enqueued_singer)

        create_enqueued_singer(queue_id=self.queue.queue_id,
                                    singer_id=singer_id,
                                    enqueued_singer_id=enqueued_singer.enqueued_singer_id,
                                    queue_position=enqueued_singer.position)

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