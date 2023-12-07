def cleanNAN(data):
    if type(data) == float:
        return None
    return data

def process_locations(locations):
    """
        School/Locations

        acronym - string
        name - string
        latitude - string
        longitude - string
        documented_coach - boolean
        head_coaches - reference[]
        assistant_coaches - reference[]
        location - string
        location_map - string
        provider - string
        storage - string
        stored - string
        special_location - string
    """
    loc_data = []

    for location in locations:
        loc_data.append({
            "acronym": location['Code'],
            "name": location['School'],
            "latitude": location['Latitude'],
            "longitude": location['Longitude'],
            "documented_coach": True if location['Document Status'] == "Documented" else False,
            "head_coaches": [],
            "assistant_coaches": [],
            "location": location['Location'],
            "location_map": location['Location Map'],
            "provider": location['Provider'],
            "storage": cleanNAN(location['Storage']),
            "stored": cleanNAN(location['Is our ball bag stored']),
            "special_location": cleanNAN(location['Emirates'])
        })
    
    return loc_data

def correctAcronym(acronym):
    if acronym == "FC 1":
        return "FC1"
    elif acronym == "FC 2":
        return "FC2"
    elif acronym == "MPH 1":
        return "MPH1"
    elif acronym == "MPH 2":
        return "MPH2"
    else:
        return acronym

def findCourtWithAcronym(acronym, programs):
    for program in programs:
        if correctAcronym(program['Court Location Abbreviation']) == acronym:
            return program['Court Location']

def findSchoolWithCourtAcronym(acronym, programs, location_data):
    for program in programs:
        if correctAcronym(program['Court Location Abbreviation']) == acronym:
            for school in location_data:
                if school['acronym'] == program['Location Acronym']:
                    return school['acronym']

def process_courts(programs, location_data):
    """
        Court

        court_id - integer
        acronym - string
        name - string
        school - reference
    """
    court_acronym_set = set()
    court_data = []

    for program in programs:
        court_acronym_set.add(correctAcronym(program['Court Location Abbreviation']))

    for acronym in court_acronym_set:
        court_data.append({
            "acronym": acronym,
            "name": findCourtWithAcronym(acronym, programs),
            "school": findSchoolWithCourtAcronym(acronym, programs, location_data)
        })
    
    return court_data