from datetime import datetime
from app.models import QueueDB, EnqueuedSingerDB, SongChoiceDB

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


def _setup_song_choices_table():
    SongChoiceDB.create_table()

def _populate_song_choices_table(choices):
    for choice in choices:
        SongChoiceDB(**choice).save()


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
        'enqueued_singer_id': 'c61b078e-4046-4ea8-bf6b-8620cf040703',
        'queue_position': 1
    },
    {
        'queue_id': '240722c4-16a4-46e5-89fd-773445d7d38e',
        'singer_id': '110974f0-9185-47c4-ae1b-f890048ea44d',
        'enqueued_singer_id': '5776f6f7-3a51-4dd4-b21c-31625887ac7f',
        'queue_position': 2
    },
    {
        'queue_id': '240722c4-16a4-46e5-89fd-773445d7d38e',
        'singer_id': 'cf298018-4c0b-4aa9-b8d4-15ea48996811',
        'enqueued_singer_id': '48cc41c0-cfe5-4c0b-bf13-6663d4fe99fa',
        'queue_position': 3
    }
]


SONG_CHOICES = [
    {
        'enqueued_singer_id': 'e2520391-b24c-41ca-96c0-1e8813272d85',
        'song_id': 'song-choice-1',
        'position': 1
    },
    {
        'enqueued_singer_id': 'e2520391-b24c-41ca-96c0-1e8813272d85',
        'song_id': 'song-choice-2',
        'position': 2
    },
    {
        'enqueued_singer_id': 'e2520391-b24c-41ca-96c0-1e8813272d85',
        'song_id': 'song-choice-3',
        'position': 3
    }
]