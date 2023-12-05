from flask import Blueprint, request, jsonify

algo = Blueprint('algo', __name__, url_prefix='/algo')

@algo.route("/", methods=("GET",))
def index():
    return "Algorithm"
