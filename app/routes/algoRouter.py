from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.utils import convert

algo = Blueprint('algo', __name__, url_prefix='/algo')

@algo.route("/", methods=("GET",))
@jwt_required()
def index():
    return "Algorithm"

@algo.route("/convert", methods=("POST",))
@jwt_required()
def _convert():
    if 'input' not in request.files:
        return "no file provided"
    file = request.files['input']
    return convert(file)
