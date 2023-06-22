import os 
import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
from databases import Database
from .models import SingerSchema


DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()
singers = Table(
    "singers",
    metadata,
    Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4),
    Column('first_name', String(50)),
    Column('last_name', String(50)),
    Column('stage_name', String(100)),
    Column('email', String(100)),
    Column('created_date', DateTime, default=func.now(), nullable=False)
)

database = Database(DATABASE_URL)


async def create_singer_db(data: SingerSchema):
    query = singers.insert().values(
        first_name=data.first_name, 
        last_name=data.last_name,
        stage_name=data.stage_name,
        email=data.email)
    
    return await database.execute(query=query)


async def get_singer_db(id: uuid.UUID):
    query = singers.select().where(id == singers.c.id)

    return await database.fetch_one(query=query)


async def get_all_singers_db():
    query = singers.select()

    return await database.fetch_all(query=query)


async def update_singer_db(id: uuid.UUID, data: SingerSchema):
    query = (
        singers
        .update()
        .where(id == singers.c.id)
        .values(first_name=data.first_name, 
                last_name=data.last_name, 
                stage_name=data.stage_name, 
                email=data.email)
    )

    return await database.execute(query=query)


async def delete_singer_db(id: uuid.UUID):
    query = singers.delete().where(id == singers.c.id)

    return await database.execute(query=query)
