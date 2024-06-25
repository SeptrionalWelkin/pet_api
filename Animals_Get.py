import requests
import json
# Sending a GET request to our API
response = requests.get(url="http://127.0.0.1:5000/animals")
# printing out the response
print(response.text)

response = requests.get(url="http://127.0.0.1:5000/animals/Dog")
print(response.text)

response = requests.get(url="http://127.0.0.1:5000/animals/Bird")
print(response.text)
