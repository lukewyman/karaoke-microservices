import logging 
import os 
import motor.motor_asyncio
from bson import ObjectId


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_db():
    mongo_hostname = os.environ['MONGO_HOSTNAME']
    mongo_port = os.environ['MONGO_PORT']
    mongo_username = os.environ['MONGO_USERNAME']
    mongo_password = os.environ['MONGO_PASSWORD']
    mongo_architecture = os.environ.get('MONGO_ARCHITECTURE', 'standalone')
    mongo_querystring   = '/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
    if mongo_architecture == 'standalone':
        mongo_querystring = ''

    mongo_url = f'mongodb://{mongo_username}:{mongo_password}@{mongo_hostname}:{mongo_port}{mongo_querystring}'
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    return client['karaoke']


async def get_all_songs_db():
    songs = await get_db()['song-library'].find({}).to_list(None)
    return songs


async def get_song_db(song_id):
    return await get_db()['song-library'].find_one({'_id': song_id})


async def create_song_db(song: dict) -> dict:
    new_song = await get_db()['song-library'].insert_one(song)
    inserted_song = await get_db()['song-library'].find_one({'_id': new_song.inserted_id})
    logger.info(f'Inserted Song: {inserted_song}')

    return inserted_song


async def update_song_db(id: str, song_data: dict):
    logger.info(f'Song ID: {id}, Song data: {song_data}')
    song_library = get_db()['song-library']
    update_result = await song_library.update_one(
        {'_id': id}, {'$set': song_data}
    )
    logger.info(f'Update Result: {update_result}')

    return update_result


async def delete_song_db(id: str):
    logger.info(f'Song ID: {id}')
    song_library = get_db()['song-library']
    delete_result = await song_library.delete_one({'_id': id})
    logger.info(f'Delete Result: {delete_result}')

    return delete_result
    