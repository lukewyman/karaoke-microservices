import uuid
import logging 
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas 
from .database import SessionLocal, engine 


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if engine:
    models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/health')
async def health_check():
    return JSONResponse(status_code=200, content='OK')


@app.post("/singers/", response_model=schemas.Singer)
def create_singer(singer: schemas.SingerCreate, db: Session = Depends(get_db)):
    db_singer = crud.get_singer_by_email(db, email=singer.email)
    if db_singer:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    return crud.create_singer(db=db, singer=singer)


@app.get("/singers/", response_model=list[schemas.Singer])
def get_singers(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    singers = crud.get_singers(db, skip=skip, limit=limit)
    return singers 


@app.get("/singers/{singer_id}", response_model=schemas.Singer)
def get_singer(singer_id: uuid.UUID, db: Session = Depends(get_db)):
    db_singer = crud.get_singer(db, singer_id=singer_id)
    if db_singer is None:
        raise HTTPException(status_code=404, detail="Singer not found.")
    return db_singer


@app.post("/singers/{singer_id}/favorites/", response_model=schemas.Favorite)
def create_singer_favorite(
    singer_id: uuid.UUID, favorite: schemas.FavoriteCreate, db: Session = Depends(get_db)
):
    return crud.create_singer_favorite(db=db, favorite=favorite, singer_id=singer_id)