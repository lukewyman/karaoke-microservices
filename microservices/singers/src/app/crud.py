import uuid
import logging 
from sqlalchemy.orm import Session 

from . import models, schemas


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_singer(db: Session, singer_id: uuid.UUID):
    return db.query(models.Singer).filter(models.Singer.id == singer_id).first()


def get_singer_by_email(db: Session, email: str):
    return db.query(models.Singer).filter(models.Singer.email == email).first()


def get_singers(db: Session, skip: int = 0, limit: int = 20):
    singers = db.query(models.Singer).offset(skip).limit(limit).all()
    print(singers)
    return singers


def create_singer(db: Session, singer: schemas.SingerCreate):
    db_singer = models.Singer(**singer.dict())
    db.add(db_singer)
    db.commit()
    db.refresh(db_singer)
    return db_singer


def create_singer_favorite(db: Session, favorite: schemas.FavoriteCreate, singer_id: int):
    db_favorite = models.Favorite(**favorite.dict(), singer_id=singer_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite