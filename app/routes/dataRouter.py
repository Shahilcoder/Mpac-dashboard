from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

dataRouter = Blueprint("data", __name__, url_prefix="/data")

@dataRouter.route("/coach/update", methods=("PUT",))
def update_coach():
    return "put"

@dataRouter.route("/coach/delete", methods=("DELETE",))
def delete_coach():
    return "delete"