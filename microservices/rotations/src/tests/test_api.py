import json
import uuid
from datetime import datetime
from starlette.testclient import TestClient
from moto import mock_dynamodb
from .data import (
    _setup_queues_table,
    _populate_queues_table,
    _setup_singers_table,
    _populate_singers_table,
    QUEUES, 
    SINGERS
)


def test_health_check(test_app: TestClient):
    response = test_app.get('/health')
    
    assert response.status_code == 200
    assert response.json() == "OK"


@mock_dynamodb
def test_start_queue(test_app: TestClient):
    _setup_queues_table()

    queue_data = {
        'location_id': str(uuid.uuid4())
    }
    response = test_app.post('/queues/', content=json.dumps(queue_data))

    assert response.status_code == 201


@mock_dynamodb
def test_get_empty_queue(test_app: TestClient):
    _setup_queues_table()
    _populate_queues_table(QUEUES)
    _setup_singers_table()

    queue_id = QUEUES[0]['queue_id']  
    response = test_app.get(f'/queues/{queue_id}')

    assert response.status_code == 200
    body = json.loads(response.content)
    assert body['queue_id'] == QUEUES[0]['queue_id']
    assert body['location_id'] == QUEUES[0]['location_id']


@mock_dynamodb
def test_enqueue_singer(test_app: TestClient):
    _setup_queues_table()
    _populate_queues_table(QUEUES)
    _setup_singers_table()
    
    singer_data = {
        'singer_id': '69400125-d093-41c1-9415-6af0168078f4'
    }
    queue_id = QUEUES[1]['queue_id']

    response = test_app.post(f'/queues/{queue_id}/singers/', 
                             content=json.dumps(singer_data))
    
    assert response.status_code == 201 
    body = json.loads(response.content)
    assert body['queue_id'] == queue_id
    assert len(body['singers']) == 1
    assert body['singers'][0]['singer_id'] == '69400125-d093-41c1-9415-6af0168078f4'
    assert body['singers'][0]['position'] == 1
    

# @mock_dynamodb
# def test_get_singer(test_app: TestClient):
#     _setup_queues_table()
#     _populate_queues_table(QUEUES)
#     _setup_singers_table()
#     _populate_singers_table(SINGERS)


# @mock_dynamodb
# def test_remove_singer(test_app: TestClient):
#     pass 