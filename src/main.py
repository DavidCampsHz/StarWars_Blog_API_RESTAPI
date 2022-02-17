"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, FavoriteCharacter, FavoritePlanet, Planet, Character

#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#GET All
@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_user = list(map(lambda x: x.serialize(), users))

    return jsonify(all_user), 200

@app.route('/character', methods=['GET'])
def get_character():
    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    planet_name_query = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet_name_query))
    return jsonify(all_planets), 200

@app.route('/user/favoriteplanet', methods=['GET'])
def get_favorite_planet():

    favorites_planets = FavoritePlanet.query.all()
    all_favorites_planet = list(map(lambda x: x.serialize(), favorites_planets))

    return jsonify(all_favorites_planet), 200

@app.route('/user/favoritecharacter', methods=['GET'])
def get_favorite_character():

    favorites_characters = FavoriteCharacter.query.all()
    all_favorites_character = list(map(lambda x: x.serialize(), favorites_characters))

    return jsonify(all_favorites_character), 200

#GET SINGLE
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_single(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    return jsonify(planet.serialize()), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_single(character_id):
    character = Character.query.filter_by(character_id=character_id).first()
    return jsonify(character.serialize()), 200

#POST
@app.route('/user', methods=['POST'])
def create_user():
    request_body_user = request.get_json()
    new_user = User(email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/favoriteplanet', methods=['POST'])
def create_favorite_planet():
    request_body_planet = request.get_json()
    new_planet = FavoritePlanet(user_id=request_body_planet["user_id"], planet_id=request_body_planet["planet_id"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(request_body_planet), 200

@app.route('/user/favoritecharacter', methods=['POST'])
def create_favorite_character():
    request_body_character = request.get_json()
    new_character = FavoriteCharacter(user_id=request_body_character["user_id"], character_id=request_body_character["character_id"])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(request_body_character), 200

#PUT - Update a single record
@app.route('/user/<int:id>', methods=['PUT'])
def modify_user(id):
    request_body_user = request.get_json()

    updated_user = User.query.get(id)
    if updated_user is None:
        raise APIException('User not found', status_code=404)

    if "email" in request_body_user:
        updated_user.email = request_body_user["email"]
    db.session.commit()
    return jsonify(request_body_user), 200

#DELETE - Remove a single record
@app.route('/user/favoriteplanet/<int:id>', methods=['DELETE'])
def remove_sing_planet(id):
    remove_single_planet = FavoritePlanet.query.filter_by(id=id).first()
    print("this is the planet to be removed", id)
    #remove_single_planet = Planet.query.filter_by(planet_id=planet_id).delete()
    db.session.delete(remove_single_planet)
    db.session.commit()
    return jsonify(remove_single_planet.serialize()), 200

@app.route('/user/favoritecharacter/<int:id>', methods=['DELETE'])
def remove_sing_character(id):
    remove_single_character = FavoriteCharacter.query.filter_by(id=id).first()
    print("this is the character to be removed", id)
    #remove_single_planet = Planet.query.filter_by(planet_id=planet_id).delete()
    db.session.delete(remove_single_character)
    db.session.commit()
    return jsonify(remove_single_character.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
