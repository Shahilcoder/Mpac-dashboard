from app.db import db

def upload_algorithm_output(programs):
    """
        uploads the output given by the algorithm into mongodb
        @input
        programs: list of dictonaries of programs updated with coach assigned
    """
    db.programs.insert_many(programs)
