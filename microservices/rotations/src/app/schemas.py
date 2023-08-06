import uuid 
from pydantic import BaseModel


class QueueBase(BaseModel):
    location_id: str 
    
    

class QueueCreate(QueueBase):
    pass 



