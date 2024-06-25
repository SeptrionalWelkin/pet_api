import requests
import json
# Info of the book
payloads = [
            {
                'name': 'Lady Puppington III',
                'age': '2',
                'type' : 'Dog',
                'breed': 'Cavoodle'
            },
            {
                'name': 'Lord Kittington IV',
                'age': '1',
                'type': 'Cat',
                'breed': 'Domestic Short Hair Cat'
            },
            {
                'name': 'Lady Bluebell V',
                'age': '10',
                'type': 'Dog',
                'breed': 'Jack Russell Cavalier'
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
