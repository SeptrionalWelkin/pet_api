from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
# defining URL or Path to save our DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///animals.db"
# Creating DB instance to reference throughout the code
db = SQLAlchemy(app)

#The following code block is used to create a db instance from flask_sqlalchemy and use it to define our animal table.
# Define a model class
class Animal(db.Model):
   # Using name as a primary key
   name = db.Column(db.String(150), primary_key=True)
   age = db.Column(db.Integer)
   type = db.Column(db.String(150))
   breed = db.Column(db.String(150))

   @property
   def as_json(self):
       """ Returns object data in a serializable format
       """
       return {
           'name': self.name,
           'age': self.age,
           'type': self.type,
           'breed': self.breed
       }

# If the DB doesn't exist recreate it else don't overwrite it
if not os.path.exists('animals.db'):
   with app.app_context():
       db.create_all()

@app.route('/animals', methods=['POST', 'GET'])
def animal(methodType):
    with app.app_context():
        if methodType == 'POST':
            # POST request for adding animal to DB
            try:
               # Getting user-passed data
               payload = request.get_json()
               # Creating a animal object
               animal = Animal(name=payload['name'],
                           age=payload['age'],
                           type=payload['type'],
                           breed=payload['breed'])

            except Exception as e:
                raise TypeError("Data in unexpected format")
                return

               # add new animal object to DB
            db.session.add(animal)
               # commit db to save changes
            db.session.commit()
               # return the same animal to let the user know that it has been added to the DB
            return jsonify(json.dumps(payload))

        elif methodType == 'GET':
            # GET request for getting all animals from DB
            animals = Animal.query.all()
            # serializing objects so that we can send them in a JSON object
            serialized_animals = [animal.as_json for animal in animals]
            return serialized_animals

@app.route('/animals/<type_requested>', methods=['GET'])
def get_animal_by_type(type_requested):
   # GET request for getting certain animals from DB
    animals = Animal.query.filter_by(type=type_requested)
    # serializing objects so that we can send them in a JSON object
    serialized_animals = [animal.as_json for animal in animals]
    return jsonify(serialized_animals)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
