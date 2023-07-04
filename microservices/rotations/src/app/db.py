import boto3


dynamo_resource = None 

def init_dynamodb():
    global dynamo_resource
    if dynamo_resource is None:
        dynamo_resource = boto3.resource('dynamodb', region_name='us-west-2')


def create_rotation_db(rotation):
    rotation_dynamo = {
        'rotation_id': rotation.rotation_id,
        'created_date': rotation.created_date,
        'current_singer_index': rotation.current_singer_index
    }
    return None


def get_rotation_db(rotation_id):
    return None 