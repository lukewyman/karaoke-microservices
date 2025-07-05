import requests 
import os
import uuid


SONG_CHOICES_URL = os.environ['SONG_CHOICES_SERVICE']
SINGERS_URL = os.environ['SINGERS_SERVICE']


def post_song_choice(queue_id: uuid.UUID, singer_id: uuid.UUID, song_id: str):
    song_choice_create = {'song_id': song_id}
    response = requests.post(f'{SONG_CHOICES_URL}/queues/{queue_id}/singers/{singer_id}', 
                             data=song_choice_create)
    
    return response.json()


def get_next_song_choice(queue_id: uuid.UUID, singer_id: uuid.UUID):
    response = requests.get(f'{SONG_CHOICES_URL}/queues/{queue_id}/singers/{singer_id}/songs/next')

    if response.status_code == 404:
        raise ValueError(response.json())

    return response.json()


def delete_song_choice(queue_id: uuid.UUID, singer_id: uuid.UUID, song_id: str):
    response = requests.delete(f'{SONG_CHOICES_URL}/queues/{queue_id}/singers/{singer_id}/songs/{song_id}') 

    if response.status_code == 404:
        raise ValueError(response.json())
    
    return response.json()


def get_singer(singer_id: uuid.UUID):
    response = requests.get(f'{SINGERS_URL}/singers/{singer_id}')

    if response.status_code == 404:
        raise ValueError(response.json())

    return response.json()

