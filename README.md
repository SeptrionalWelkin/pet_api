# pet_api

Requirements

local serverless dynanmo:

    serverless plugin install -n serverless-dynamodb

**Run Docker image of dynamodb**
docker run -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -inMemory -sharedDb

**Run the Serverless** 
npm run dev

**Go to app in browser or Postman etc**
http://localhost:3000