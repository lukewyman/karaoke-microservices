from datetime import datetime
from app.models import QueueDB, EnqueuedSingerDB

def _setup_queues_table():
    QueueDB.create_table()


def _populate_queues_table(queues):
    for queue in queues:
        QueueDB(**queue).save()

def _setup_enqueued_singers_table():
    EnqueuedSingerDB.create_table()


def _populate_enqueued_singers_table(enqueued_singers):
    for enqueued_singer in enqueued_singers:
        EnqueuedSingerDB(**enqueued_singer).save()


QUEUES = [
    {
        'queue_id': '112013d5-7430-4344-af3c-93e45914e4ca',
        'location_id': 'e75c9cf2-4e6f-41f7-93ea-5b7cb8dacd44',
        'event_date': datetime.now(),
        'current_singer_index': 0
    },
    {
        'queue_id': '240722c4-16a4-46e5-89fd-773445d7d38e',
        'location_id': '3d9672a4-bc6f-40ec-b104-959789b9362f',
        'event_date': datetime.now(),
        'current_singer_index': 0
    }
]


ENQUEUED_SINGERS = [
    {
        'queue_id': '240722c4-16a4-46e5-89fd-773445d7d38e',
        'singer_id': '69400125-d093-41c1-9415-6af0168078f4',
        'queue_position': 1
    },
    {
        'queue_id': '240722c4-16a4-46e5-89fd-773445d7d38e',
        'singer_id': '110974f0-9185-47c4-ae1b-f890048ea44d',
        'queue_position': 2
    },
    {
        'queue_id': '240722c4-16a4-46e5-89fd-773445d7d38e',
        'singer_id': 'cf298018-4c0b-4aa9-b8d4-15ea48996811',
        'queue_position': 3
    }
]

