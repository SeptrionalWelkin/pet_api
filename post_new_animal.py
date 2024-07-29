import json
from utils import database_utils, field_validation
from boto3.dynamodb.conditions import Key


def post_new_animal(event, context):
    endpoint = 'http://localhost:8000'
    table = database_utils.DatabaseClient(endpoint).database_client().Table('animalsTable')

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

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
