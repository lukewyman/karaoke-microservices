import uuid 
from pydantic import BaseModel

class SongChoiceCreate(BaseModel):
    song_id: str

class SongChoice(SongChoiceCreate):
    queue_id: uuid.UUID
    singer_id: uuid.UUID
    song_id: str
    position: int 

class SongChoiceUpdate(BaseModel):
    new_position: int