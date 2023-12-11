from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.utils.algo import convert
from app.utils.upload.helpers import process_excel_file_into_dictlist

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
    coaches, locations, programs = process_excel_file_into_dictlist(file)
    return convert(coaches, locations, programs)
    # return "Upload successfull"
