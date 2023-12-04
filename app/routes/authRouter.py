import datetime

import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.db import db

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/sign-up", methods=("POST",))
def signUP():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username is None or password is None:
        return jsonify({"msg": "Please provide username and password"}), 403
    
    users = db.users
    user = users.find_one({"username": username})

    if user is not None:
        return jsonify({"msg": "User already exists"}), 403
    
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    users.insert_one({
        "username": username,
        "password": hashed_password.decode('utf-8')
    })

    return jsonify({"msg": "User Sign up successfully"}), 201


@auth.route("/sign-in", methods=("POST",))
def signIn():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username is None or password is None:
        return jsonify({"msg": "Please provide username and password"}), 403
    
    users = db.users
    user = users.find_one({"username": username})

    if user is None:
        return jsonify({"msg": "User does not exists"}), 404

    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"msg": "Incorrect password"}), 401

    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=4))
    return jsonify(access_token=access_token)


# Testing
# @auth.route("/protected", methods=("GET",))
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
