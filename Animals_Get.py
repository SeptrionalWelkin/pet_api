import requests
import json

apiEndpoint = "http://localhost:3000"

# Sending a GET request to our API
response = requests.get(url=apiEndpoint+"/animals")
# printing out the response
print(response.text)

response = requests.get(url=apiEndpoint+"/animals/Dog")
print(response.text)

response = requests.get(url=apiEndpoint+"/animals/Bird")
print(response.text)
