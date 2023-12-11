from app.db import db

def upload_algorithm_output(programs):
    """
        uploads the output given by the algorithm into mongodb
        @input
        programs: list of dictonaries of programs updated with coach assigned
    """
    for program in programs:
        db.programs.find_one_and_update({{'program_id': program['program_id']}, {"$set": program}})
