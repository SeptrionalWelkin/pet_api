import json
from utils import database_utils
from boto3.dynamodb.conditions import Key


def get_all_animals_by_type(event, context):
    endpoint = 'http://localhost:8000'
    table = database_utils.DatabaseClient(endpoint).database_client().Table('animalsTable')

    path_parameters = event.get('pathParameters', {})
    animalType = path_parameters.get('type')

    response = table.query(
        IndexName="typeIndex",
        KeyConditionExpression=Key('type').eq(animalType)
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }