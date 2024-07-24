import json
from utils import field_validation

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
        animalType = path_parameters.get('type').strip()

        # Strips leading and trailing whitespace from values
        cleaned_data = {k: v.strip() for k, v in data.items()}

        input_validation = field_validation.field_validation(cleaned_data, animalType)

        # Validate fields
        if input_validation[0] is False:
            raise ValueError(input_validation[1])

        # Checks if Animal of this name and type exists
        response = table.query(
            KeyConditionExpression=Key('name').eq(cleaned_data['name']) & Key('type').eq(animalType))

        if len(response['Items']) != 0:
            raise ValueError("Animal already exists!")

        item = {
            'name': cleaned_data['name'],
            'type': animalType,
            'breed': cleaned_data['breed'],
            'age': cleaned_data['age']
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
