import boto3


class DatabaseClient:
    def __init__(self, endpoint):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url= endpoint)


    def database_client(self):
        return self.dynamodb
