"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

import json

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=["POST"])
def signup():
    data = request.data
    data = json.loads(data)

    new_user = User(
        username = data['username'],
        email = data['email'],
        password = data['password'],
        is_active = True
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize())

@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    #Meto en una variable el contenido al cual accedo desde la base de datos
    user = User.query.filter_by(username = username, password = password).first()
    print(user) #la representacion esta definida en models.py

    if user == None:
        return jsonify({"msg": "El usuario o la contrasenia estan equivocadas"}), 401

    # crea un nuevo token con el id de usuario dentro
    access_token = create_access_token(identity=username)
    print(access_token)
    return jsonify({ "token": access_token, "username": username })

@api.route("/private", methods=["GET"])
@jwt_required()
def protected():
    # Accede a la identidad del usuario actual con get_jwt_identity
    response_body = {
        "current_user" : get_jwt_identity(),
        "tokenCorrecto" : True
    }
    
    
    return jsonify(response_body), 200