from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.db import db

dataRouter = Blueprint("data", __name__, url_prefix="/data")

@dataRouter.route("/coach/all", methods=("GET",))
@jwt_required()
def get_coaches():
    coach_coll = db.coaches
    coaches = list(coach_coll.find(projection={'_id': False, 'coach_id': True, 'coach_name': True}))
    if len(coaches) == 0:
        return jsonify(msg="Coaches not found"), 404

    return jsonify(coaches=coaches), 200

@dataRouter.route("/coach/add", methods=("POST",))
@jwt_required()
def add_coach():
    payload = request.json

    coach_coll = db.coaches
    payload['coach_id'] = f"C{coach_coll.count_documents({}) + 1}"
    coach_coll.insert_one(payload)

    return jsonify(msg="Coach Added"), 201

@dataRouter.route("/coach/update", methods=("PUT",))
@jwt_required()
def update_coach():
    payload = request.json

    coach_coll = db.coaches
    doc = coach_coll.find_one_and_update({'coach_id': payload['coach_id']}, {'$set': payload})
    if doc is None:
        return jsonify(msg="Coach not found"), 404

    return jsonify(msg="Coach Updated"), 200

@dataRouter.route("/coach/delete/<coach_id>", methods=("DELETE",))
@jwt_required()
def delete_coach(coach_id):
    coach_coll = db.coaches
    doc = coach_coll.find_one_and_delete({'coach_id': coach_id})
    if doc is None:
        return jsonify(msg="Coach not found"), 404

    return jsonify(msg="Coach Deleted"), 200

@dataRouter.route("/court/all", methods=("GET",))
@jwt_required()
def get_courts():
    court_coll = db.courts
    courts = list(court_coll.find(projection={'_id': False}))
    if len(courts) == 0:
        return jsonify(msg="Courts not found"), 404

    return jsonify(courts=courts), 200

@dataRouter.route("/court/add", methods=("POST",))
@jwt_required()
def add_court():
    payload = request.json

    court_coll = db.courts
    doc = court_coll.find_one({'acronym': payload['acronym']})
    if doc is not None:
        return jsonify(msg="Court already exists"), 403
    
    court_coll.insert_one(payload)
    return jsonify(msg="Court Added"), 201

@dataRouter.route("/court/update", methods=("PUT",))
@jwt_required()
def update_court():
    payload = request.json

    court_coll = db.courts
    doc = court_coll.find_one_and_update({'acronym': payload['acronym']}, {"$set": payload})
    if doc is None:
        return jsonify(msg="Court not found"), 404

    return jsonify(msg="Court Updated"), 200

@dataRouter.route("/court/delete/<acronym>", methods=("DELETE",))
@jwt_required()
def delete_court(acronym):
    court_coll = db.courts
    doc = court_coll.find_one_and_delete({'acronym': acronym})
    if doc is None:
        return jsonify(msg="Court not found"), 404

    return jsonify(msg="Court Deleted"), 200

@dataRouter.route("/school/all", methods=("GET",))
@jwt_required()
def get_schools():
    school_coll = db.schools
    schools = list(school_coll.find(projection={'_id': False, 'acronym': True, 'name': True, 'courts': True}))
    if len(schools) == 0:
        return jsonify(msg="Schools not found"), 404

    return jsonify(schools=schools), 200

@dataRouter.route("/school/add", methods=("POST",))
@jwt_required()
def add_school():
    payload = request.json

    school_coll = db.schools
    doc = school_coll.find_one({'acronym': payload['acronym']})
    if doc is not None:
        return jsonify(msg="School already exists"), 403
    
    school_coll.insert_one(payload)
    return jsonify(msg="School Added"), 201

@dataRouter.route("/school/update", methods=("PUT",))
@jwt_required()
def update_school():
    payload = request.json

    school_coll = db.schools
    doc = school_coll.find_one_and_update({'acronym': payload['acronym']}, {"$set": payload})
    if doc is None:
        return jsonify(msg="School not found"), 404

    return jsonify(msg="School Updated"), 200

@dataRouter.route("/school/delete/<acronym>", methods=("DELETE",))
@jwt_required()
def delete_school(acronym):
    school_coll = db.schools
    doc = school_coll.find_one_and_delete({'acronym': acronym})
    if doc is None:
        return jsonify(msg="School not found"), 404

    return jsonify(msg="School Deleted"), 200

@dataRouter.route("/program/all", methods=("GET",))
@jwt_required()
def get_programs():
    program_coll = db.programs
    programs = list(program_coll.find(projection={'_id': False}))
    if len(programs) == 0:
        return jsonify(msg="Schools not found"), 404

    return jsonify(programs=programs), 200
