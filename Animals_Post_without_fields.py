import requests
import json
# Info of the book
payloads = [
            {
                'name': 'Rex',
                'type' : 'Dog',
                'breed': 'German Shepard'
            }
]

# header of our post request indicating content type to be JSON
headers = {'Content-type': 'application/json'}
# Sending a post request to our API
for payload in payloads:
    response = requests.post(url='http://127.0.0.1:5000/add_animal',
                        data=json.dumps(payload),
                        headers=headers)
    # Printing out the response.
    print(response.text)
