from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.db import db

dataRouter = Blueprint("data", __name__, url_prefix="/data")

@dataRouter.route("/coach/update", methods=("PUT",))
@jwt_required()
def update_coach():
    payload = request.json

    coach_coll = db.coaches
    coach_coll.update_one({'coach_id': payload['coach_id']}, {'$set': payload})
    return jsonify(msg="Coach Updated"), 200

@dataRouter.route("/coach/delete/<coach_id>", methods=("DELETE",))
@jwt_required()
def delete_coach(coach_id):
    coach_coll = db.coaches
    coach_coll.delete_one({'coach_id': coach_id})

    return jsonify(msg="Coach Deleted"), 200
