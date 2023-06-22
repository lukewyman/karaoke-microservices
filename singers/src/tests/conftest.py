import pytest
import pytest_asyncio
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine, select 
from sqlalchemy.orm.session import sessionmaker
from starlette.testclient import TestClient


from app.main import app

@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client


test_db = factories.postgresql_proc(port=None, dbname='test_db')


