import json
from utils import database_utils


def get_all_animals(event, context):
    endpoint = 'http://localhost:8000'
    table = database_utils.DatabaseClient(endpoint).database_client().Table('animalsTable')

    # Scan is an expensive operation, only used for POC
    response = table.scan()

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
