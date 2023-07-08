import uuid
from pydantic import BaseModel


class FavoriteBase(BaseModel):
    song_id: str 
    position: int 


class FavoriteCreate(FavoriteBase):
    pass 


class Favorite(FavoriteBase):
    id: int
    singer_id: uuid.UUID 

    class Config:
        orm_mode = True 


class SingerBase(BaseModel):
    email: str 
    first_name: str 
    last_name: str 
    stage_name: str 


class SingerCreate(SingerBase):
    pass 


class Singer(SingerBase):
    id: uuid.UUID 
    favorites: list[Favorite] = []

    class Config:
        orm_mode = True 