#from clean_whitespace import clean_whitespace
def field_validation(data, animalType):
    #data expected is a json in the following format
    # {
    #     "name": "Lord Kittington IV",
    #     "breed": "Domestic Short Hair Cat",
    #     "age": "1"
    # }
    # and animalType is a string

    is_valid_input = False
    message = ""
    #cleaned_data = clean_whitespace(data)

    #Checks all fields are available
    if ('name' not in data
            or 'breed' not in data
            or 'age' not in data
            or data['name'] == ""
            or data['breed'] == ""):

        message += "Missing fields: "

        if 'name' not in data or data['name'] == "":
            message += "Name "

        if 'breed' not in data or data['breed'] == "":
            message += "Breed "

        if 'age' not in data:
            message += "Age "


    #Checks all fields are valid
    elif (len(data['name']) > 50
          or len(data['breed']) > 50
          or (not data['age'].isnumeric() or len(data['age']) > 2)):
        if len(data['name']) > 50:
            message += "Name too long "
        if len(data['breed']) > 50:
            message += "Breed too long "
        if not data['age'].isnumeric() or len(data['age']) > 2:
            message += "Invalid Age "
        if len(animalType) > 50:
            message += "Animal type too long "

    else:
        is_valid_input = True
        message += "Valid input"

    return is_valid_input, message

