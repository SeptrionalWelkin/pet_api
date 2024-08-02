import requests
import json
from utils import load_file
from jsondifftest import diff


def test_get_animals():
    animals_DB = load_file.load_file("output", "test_output_db.json")

    headers = {'Content-type': 'application/json'}
    response = requests.get(url='http://localhost:3000/animal',
                            headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == animals_DB


def test_get_dogs():
    get_dog_DB = load_file.load_file("output", "test_get_dog_output_db.json")

    headers = {'Content-type': 'application/json'}
    response = requests.get(url='http://localhost:3000/animal/dog',
                            headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == get_dog_DB


def test_get_non_existent_animals():
    headers = {'Content-type': 'application/json'}
    response = requests.get(url='http://localhost:3000/animal/jabberwocky',
                            headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_post_animals():
    headers = {'Content-type': 'application/json'}
    input_animal = load_file.load_file("input", "input_animal.json")
    test_post_output_db = load_file.load_file("output", "test_post_output_db.json")

    requests.post(url='http://localhost:3000/animal/cat',
                             headers=headers,
                             json=input_animal)

    response = requests.get(url='http://localhost:3000/animal',
                            headers=headers)

    test_post_output_db.sort(key=lambda s: s['name'])
    sorted_results = response.json()
    sorted_results.sort(key=lambda s: s['name'])
    # Assert
    assert sorted_results == test_post_output_db


def test_post_empty_blank_fields():
    headers = {'Content-type': 'application/json'}

    empty_data = load_file.load_file("input", "empty_spaces_data.json")

    response = requests.post(url='http://localhost:3000/animal/whateverAnimal',
                             headers=headers,
                             json=empty_data)

    expected_error = {
        "error": "Missing fields: Name Breed "
    }
    # Assert
    assert response.json() == expected_error


def test_post_existing_animal():
    headers = {'Content-type': 'application/json'}
    existing_data = load_file.load_file("input", "existing_animal.json")

    response = requests.post(url='http://localhost:3000/animal/dog',
                             headers=headers,
                             json=existing_data)

    expected_error = {
        "error": "Animal already exists!"
    }

    # Assert
    assert response.json() == expected_error


def test_leading_trailing_spaces():
    leading_trailing_spaces_input = load_file.load_file("input", "leading_trailing_spaces.json")

    leading_trailing_spaces_output = load_file.load_file("output", "test_leading_trailing_spaces_output.json")
    headers = {'Content-type': 'application/json'}

    response = requests.post(url='http://localhost:3000/animal/angel',
                             headers=headers,
                             json=leading_trailing_spaces_input)

    # Assert
    assert response.json() == leading_trailing_spaces_output


def test_too_long_fields():
    headers = {'Content-type': 'application/json'}

    long_data = load_file.load_file("input", "long_data.json")

    response = requests.post(url='http://localhost:3000/animal/dog',
                             headers=headers,
                             json=long_data)

    expected_error = {
        "error": "Name too long Breed too long Invalid Age "
    }
    # Assert
    assert response.json() == expected_error
