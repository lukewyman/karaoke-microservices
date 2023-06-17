from bson import ObjectId
from pydantic import BaseModel, Field 


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate 
    
    @classmethod 
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('InvalidObjectId')
        return ObjectId(v)
    
    @classmethod 
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')    


class Song(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    song_title: str 
    artist: str 

    class Config:
        allow_manipulation_by_field_name = True 
        arbitrary_types = True 
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'song_title': "I Can't Get No Satisfaction",
                'artist': 'Rolling Stones'
            }
        }