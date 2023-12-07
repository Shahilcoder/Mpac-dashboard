import pandas as pd

from app.db import db

from .locations import process_locations, process_courts
from .coaches import process_coaches
from .programs import process_programs

def get_dataframes_dicts(file):
    """
        gets the three dataframes from the excel file
        @input
        file: the file object, or the file path string
    """
    df_dict = pd.read_excel(file, sheet_name=['Coaches', 'Programs', 'Locations'])
    coaches = df_dict['Coaches'].to_dict(orient='records')
    locations = df_dict['Locations'].to_dict(orient='records')
    programs = df_dict['Programs'].to_dict(orient='records')

    return coaches, locations, programs

def upload_data_to_mongodb(file):
    """
        uploads the given input excel file to mongodb
        @input
        file: the file object, or file path string
    """
    coaches, locations, programs = get_dataframes_dicts(file)

    location_data = process_locations(locations)
    court_data = process_courts(programs, location_data)
    coach_data = process_coaches(coaches, location_data)
    program_data = process_programs(programs, court_data)

    coaches_coll = db.coaches
    locations_coll = db.schools
    courts_coll = db.courts
    programs_coll = db.programs

    coaches_coll.insert_many(coach_data)
    locations_coll.insert_many(location_data)
    courts_coll.insert_many(court_data)
    programs_coll.insert_many(program_data)
