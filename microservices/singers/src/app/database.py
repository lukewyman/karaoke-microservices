import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


POSTGRES_HOSTNAME = os.environ.get('DB_HOST')
POSTGRES_PORT = os.environ.get('DB_PORT')
POSTGRES_DB = os.environ.get('DB_NAME')
POSTGRES_USERNAME = os.environ.get('DB_USER')
POSTGRES_PASSWORD = os.environ.get('DB_PASS')

# - DATABASE_URL=postgresql://singers_user:pa55w0RD@db/singers
DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, connect_args={'options': '-csearch_path={}'.format('singers')})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()