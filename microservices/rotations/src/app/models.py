from datetime import datetime
import uuid
from datetime import datetime
from pydantic import BaseModel


class EnqueuedSinger(BaseModel):
    singer_id: uuid.UUID 
    song_id: str     


class Rotation(BaseModel):
    rotation_id: uuid.UUID
    created_date: datetime
    singers: list[EnqueuedSinger]
    current_singer_index: int    
    
    # def __init__(self, rotation_id, created_date, current_index, singers):
    #     self.rotation_id = rotation_id
    #     self.singers = singers
    #     self.current_singer_index = current_index
    #     self.created_date = created_date 

    @classmethod
    def fromEmpty(cls):
        return Rotation(uuid.uuid4(), datetime.utcnow(), [None],  0)
    
    # @classmethod
    # def fromSingersList(cls, rotation_id, created_date, current_index, singers):
    #     return Rotation(rotation_id, created_date, current_index, singers)
    
    @property
    def current_singer(self):
        if len(self.singers) == 0: 
            return None
        else:
            return self.singers[self._current_singer_index]


    def add_singer(self, singer):
        if singer in self.singers:
            raise ValueError(f'Singer {singer} already in rotation.')

        self.singers.append(singer)


    def complete_performance(self):
        if self._current_singer_index == len(self.singers) -1:
            self._current_singer_index = 0
        else:
            self._current_singer_index += 1

    
    def remove_singer(self, singer):
        if singer not in self.singers:
            raise ValueError(f'Singer {singer} not in rotation, cannot be removed.')

        if self.singers.index(singer) < self._current_singer_index:
            self._current_singer_index -=1
        
        if (self.singers.index(singer) == self._current_singer_index and
            self.singers.index(singer) == len(self.singers) -1):
            self._current_singer_index = 0

        self.singers = [s for s in self.singers if s != singer]
