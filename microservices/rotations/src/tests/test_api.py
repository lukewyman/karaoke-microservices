import json
import uuid
from moto import mock_dynamodb
from .data import _setup_queues_table


def test_health_check(test_app):
    response = test_app.get('/health')
    
    assert response.status_code == 200
    assert response.json() == "OK"


@mock_dynamodb
def test_start_queue(test_app):
    _setup_queues_table()

    queue_data = {
        'location_id': str(uuid.uuid4())
    }
    response = test_app.post('/queues/', content=json.dumps(queue_data))

    assert response.status_code == 201
