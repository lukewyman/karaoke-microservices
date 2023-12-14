import uuid
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import sqlalchemy.dialects.postgresql as postgresql

from .database import Base 


class Singer(Base):
    __tablename__ = "singers"

    id = Column(postgresql.UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                index=True
                )
    email =Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    stage_name = Column(String)
