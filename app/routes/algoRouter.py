from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.utils import convert
from app.utils.upload import upload_data_to_mongodb

algoRouter = Blueprint('algoRouter', __name__, url_prefix='/algo')

@algoRouter.route("/", methods=("GET",))
@jwt_required()
def index():
    return "Algorithm"

@algoRouter.route("/convert", methods=("POST",))
@jwt_required()
def _convert():
    if 'input' not in request.files:
        return "no file provided"
    file = request.files['input']
    upload_data_to_mongodb(file)
    return "Upload successfull"
    # return convert(file)
