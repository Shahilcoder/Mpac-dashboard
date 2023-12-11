from app.db import db


def formatDate(date_string):
    if type(date_string) == str:
        items = date_string.split('-')
        return f'{items[2]}-{items[1]}-{items[0]}'
    
    return date_string.strftime("%Y-%m-%d")

def formatTime(time_string):
    if type(time_string) == str:
        return time_string
    
    return time_string.strftime("%H:%M")

def getDateList(date_string):
    if type(date_string) ==  float:
        return None
    dates = date_string.split(',')
    date_arr = []

    for date in dates:
        date_arr.append(formatDate(date.strip()))
    
    return date_arr

def getLevelId(level, levels):
    for l in levels:
        if l['level'] == level:
            return l['id']
    else:
        return None

def getAgeGroupId(age, ages):
    age = age.replace(' ', '')
    for a in ages:
        if a['age_group'] == age:
            return a['id']
    else:
        return None

def process_programs(programs, age_data, level_data):
    """
        Program

        program_id - integer
        school - reference
        court - reference
        suggested_coaches - reference[]
        assigned_coach - reference
        day - string
        start_time - time
        end_time - time
        program_name - string
        level - reference
        class_type - string
        age_group - reference
        seat_capacity - integer
        free_seats - integer
        seats_taken - integer
        start_date - date
        end_date - date
        weeks - integer
        dates_no_session - date[]
        term - string
    """

    program_counter = db.programs.count_documents({}) + 1
    # program_counter = 1
    program_data = []

    for program in programs:
        program_data.append({
            "program_id": f'P{program_counter}',
            "school": program['Location Acronym'],
            "court": program['Court Location Abbreviation'],
            "suggested_coaches": [],
            "assigned_coach": None,
            "day": program['Days'],
            "start_time": formatTime(program['Start Time']),
            "end_time": formatTime(program['End Time']),
            "program_name": program['Program'],
            "level": getLevelId(program["Level"], level_data),
            "class_type": program['Class Type'],
            "age_group": getAgeGroupId(program['Age Group'], age_data),
            "seat_capacity": program['Seat Capacity'],
            "seats_taken": program['Seats Taken'],
            "free_seats": program['Available Seats'],
            "start_date": formatDate(program['Start Date']),
            "end_date": formatDate(program['End Date']),
            "weeks": program['Weeks'],
            "dates_no_session": getDateList(program['Date does not have a sessions']),
            "term": program['Term']
        })

        program_counter += 1

    return program_data
