# from app.controllers.airlineController import *
from flask import blueprints
from flask import Flask, jsonify
from app.models.user import User

airlinebp = blueprints.Blueprint('airlinebp', __name__)

@airlinebp.route("/airlines", methods=["GET"])
def hello():
    return "Hello, World!"

@airlinebp.route("/user", methods=["get"])
def get_users():
    users = User.query.all()
    
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])