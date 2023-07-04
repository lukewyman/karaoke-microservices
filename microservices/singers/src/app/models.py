from pydantic import BaseModel
from uuid import UUID


class SingerSchema(BaseModel):
    first_name: str 
    last_name: str
    stage_name: str
    email: str 

class SingerDB(SingerSchema):
    id: UUID