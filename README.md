# pet_api

Requirements:

local serverless dynanmo:

    serverless plugin install -n serverless-dynamodb

**Run Docker image of dynamodb**

    docker run -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -inMemory -sharedDb

**Run the Serverless** 

    npm run dev

**Go to app in browser or Postman etc**

    http://localhost:3000

**Run the tests with**

    pytest handler_test.py 
    
    or for more verbose:    

    pytest -vv handler_test.py

**Future Enhancements**

    -Tests currently don't have clean up and will require the database to be cleared and reseeded/reinitialised to pass
