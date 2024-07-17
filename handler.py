import json
import animal_api

import boto3
from boto3.dynamodb.conditions import Key, Attr
#from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table('animalsTable')


def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }


def getAllAnimals(event, context):
    #Scan is an expensive operation, only used for POC
    response = table.scan()

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }


def AnimalsByTypeApi(event, context):
    #return event
    http_method = event['requestContext']['http']['method']

    if http_method == 'GET':
        return getAnimalsByType(event)
    elif http_method == 'POST':
        return postNewAnimal(event)
    else:
        return response(405, {"message": "Method Not Allowed"})


def getAnimalsByType(event, context):
    path_parameters = event.get('pathParameters', {})
    animalType = path_parameters.get('type')

    response = table.query(
        IndexName="typeIndex",
        KeyConditionExpression=Key('type').eq(animalType)
    )
    return {
        'statusCode': 200,
        #'body': json.dumps(animalType)
        'body': json.dumps(response['Items'])
    }

def postNewAnimal(event, context):

    try:
        data = json.loads(event['body'])
        path_parameters = event.get('pathParameters', {})
        animalType = path_parameters.get('type')

        # Validate input
        if ('name' not in data
                or 'breed' not in data
                or 'age' not in data):
            raise ValueError("Missing one or more required fields: 'name', 'breed' or 'age")

        # Wanting to change the following to variables to change in one spot, but for some reason it breaks the queries
        newAnimalName = data['name'],
        newAnimalType = animalType,
        newAnimalBreed = data['breed'],
        newAnimalAge = data['age']

        # Checks if Animal of this name and type exists
        response = table.query(
            KeyConditionExpression=Key('name').eq(data['name']) & Key('type').eq(animalType))

        if (len(response['Items']) != 0):
            raise ValueError("Animal already exists!")

        #
        if (not isinstance(data['name'], str)
                or not isinstance(data['breed'], str)
                or not isinstance(data['age'], str)):
            raise ValueError("One or more required fields is not in the correct string format: 'name', 'breed' or 'age")


        item={
            'name': data['name'],
            'type': animalType,
            'breed': data['breed'],
            'age': data['age']
        }

        # Save the item to DynamoDB
        table.put_item(Item=item)

        response = {
            'statusCode': 200,
            'body': json.dumps(item)
        }

        return response

    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e.response['Error']['Message'])})
        }
        # return response(500, {'error': 'Internal server error'})

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
        #return response(500, {'error': 'Internal server error'})
