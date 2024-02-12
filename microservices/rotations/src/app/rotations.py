import uuid
from .domain import Queue, QueueCreate, EnqueuedSinger
from .crud import (
    create_enqueued_singer,
    create_queue,
    delete_enqueued_singer,
    get_queue,
    get_enqueued_singers,
    update_enqueued_singers,
    update_queue
)
from .mappers import (to_enqueued_singer_dbs, 
                      to_enqueued_singers, 
                      to_queue_db)

class Rotations:

    def __init__(self, queue: Queue) -> None:
        self.queue = queue


    @classmethod
    def new(self, queue_create: QueueCreate):
        queue = create_queue(queue_create)
        return Rotations(queue=queue)
    

    @classmethod
    def from_db(self, queue_id: uuid.UUID):
        queue = get_queue(queue_id=queue_id)
        queue.singers = to_enqueued_singers(get_enqueued_singers(queue_id))
        return Rotations(queue=queue)


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
        
        position = len(self.queue.singers) + 1

        enqueued_singer = create_enqueued_singer(queue_id=self.queue.queue_id,
                                    singer_id=singer_id,
                                    enqueued_singer_id=uuid.uuid4(),
                                    queue_position=position)
        
        self.queue.singers.append(enqueued_singer)
    

    def complete_performance(self):
        if self.queue.current_singer_index == len(self.queue.singers) - 1:
            self.queue.current_singer_index = 0
        else:
            self.queue.current_singer_index += 1

        update_queue(to_queue_db(self.queue))


    def remove_singer(self, singer_id: uuid.UUID):
        if self._get_singer_index(singer_id) < 0:
            raise ValueError(f'Singer with id {singer_id} is not in the queue.')

        if self._get_singer_index(singer_id) < self.queue.current_singer_index:
            self.queue.current_singer_index -= 1

        if (self._get_singer_index(singer_id) == self.queue.current_singer_index and
            self._get_singer_index(singer_id) == len(self.queue.singers) - 1):
            self.queue.current_singer_index = 0

        for singer in self.queue.singers:
            if self._get_singer_index(singer.singer_id) > self._get_singer_index(singer_id):
                singer.position -= 1 

        update_queue(to_queue_db(self.queue))
        delete_enqueued_singer(self.queue.queue_id, len(self.queue.singers))
        self.queue.singers = [s for s in self.queue.singers if s.singer_id != singer_id]
        
        update_enqueued_singers(to_enqueued_singer_dbs(self.queue.queue_id, self.queue.singers))
        