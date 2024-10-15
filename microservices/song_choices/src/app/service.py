import requests
import os 

SONG_LIBRARY_URL = os.environ['SONG_LIBRARY_SERVICE']

def get_song(song_id: str):
    response = requests.get(f'{SONG_LIBRARY_URL}/songs/{song_id}') 

    if response.status_code == 404:
        raise ValueError(response.json())
    
    return response.json()