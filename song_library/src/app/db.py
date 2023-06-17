import logging 
import os 
import motor.motor_asyncio
from bson import ObjectId


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_db():
    docdb_endpoint = os.environ['DOCDB_ENDPOINT']
    docdb_port     = os.environ['DOCDB_PORT']
    docdb_username = os.environ['DOCDB_USERNAME']
    docdb_password = os.environ['DOCDB_PASSWORD']
    docdb_suffix   = '/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
    if docdb_endpoint == 'mongo':
        docdb_suffix = ''

    docdb_url = f'mongodb://{docdb_username}:{docdb_password}@{docdb_endpoint}:{docdb_port}{docdb_suffix}'

    client = motor.motor_asyncio.AsyncIOMotorClient(docdb_url)
    return client['karaoke']


async def get_all_songs():
    songs = await get_db()['song-library'].find({}).to_list(None)
    return songs


async def get_song(song_id):
    return await get_db()['song-library'].find_one({'_id': song_id})


async def create_song(song: dict) -> dict:
    new_song = await get_db()['song-library'].insert_one(song)
    inserted_song = await get_db()['song-library'].find_one({'_id': new_song.inserted_id})
    logger.info(f'Inserted Song: {inserted_song}')

    return inserted_song


async def update_song(id: str, song_data: dict):
    logger.info(f'Song ID: {id}, Song data: {song_data}')
    song_library = get_db()['song-library']
    update_result = await song_library.update_one(
        {'_id': id}, {'$set': song_data}
    )
    logger.info(f'Update Result: {update_result}')

    return update_result


async def delete_song(id: str):
    logger.info(f'Song ID: {id}')
    song_library = get_db()['song-library']
    delete_result = await song_library.delete_one({'_id': id})
    logger.info(f'Delete Result: {delete_result}')

    return delete_result
    