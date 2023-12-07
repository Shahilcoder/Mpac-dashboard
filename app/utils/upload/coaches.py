import datetime

def cleanNAN(data):
    if type(data) == float:
        return None
    return data

age_counter = 1
age_list = ['2-5', '5-7', '8-11', '12-18', '15-18', '18+']

ages = []

for age in age_list:
    ages.append({
        "id": age_counter,
        "age_group": age
    })
    age_counter += 1

def getDaysoff(daysString):
    if type(daysString) == float:
        return []
    return daysString.replace(" ", "").split(",")

def getAgeGroup(age_group):
    if type(age_group) == float:
        return None
    
    age_group = age_group.replace(" ", "")
    if age_group == "3-5":
        age_group = "2-5"

    for age in ages:
        if age['age_group'] == age_group:
            return age['id']
    else:
        return None

def getLocationIds(location_string, location_data):
    if type(location_string) == float:
        return None
    
    loc_ids = []
    loc_array = location_string.split(",")

    for loc_acronym in loc_array:
        for location in location_data:
            if location['acronym'] == loc_acronym:
                loc_ids.append(location['acronym'])
                break
    
    loc_ids.sort()
    
    return loc_ids

def getNotWorkingPeriod(period_string):
    if type(period_string) == float:
        return None
    
    months = ['Jan', 'Feb', 'March', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    periods = period_string.split('&')
    date_arr = []

    for period in periods:
        month = period.strip()
        monthNumber = 0

        for i in range(len(months)):
            if months[i] == month:
                monthNumber = i + 1
                break

        date_arr.append(datetime.datetime.strptime(f'01 {monthNumber} 2023', '%d %m %Y').date().strftime('%Y-%m-%d'))
    
    return date_arr

def process_coaches(coaches, location_data):
    """
        Coach

        coach_id - string
        coach_name - string
        is_head - boolean
        is_documented - boolean
        is_fulltime - boolean
        work_hours - integer
        days_off - list(str)
        age_group - reference
        locations - reference
        visa_status - string
        has_transport - boolean
        not_working_period - [date, date]
        remarks - string
        remarks2 - string
    """
    coach_counter = 1
    coach_data = []

    for coach in coaches:
        coach_data.append({
            "coach_id": f'C{coach_counter}',
            "coach_name": coach['Coach Name'],
            "is_head": True if coach['Role'] == "Head Coach" else False,
            "is_documented": True if coach['Profile'] == "Documented" else False,
            "is_fulltime": True if coach['Employment Status'] == "Full Time" else False,
            "work_hours": coach['Hours of work'],
            "days_off": getDaysoff(coach['Days Off']),
            "age_group": getAgeGroup(coach['Age Group']),
            "locations": getLocationIds(coach['Locations'], location_data),
            "visa_status": coach['Visa StaTus'],
            "has_transport": True if coach['Transport'] == "Own Transport" else False,
            "not_working_period": getNotWorkingPeriod(coach['Period Not contracted to work']),
            "remarks": cleanNAN(coach['Remarks']),
            "remarks2": cleanNAN(coach['Remarks 2'])
        })

        coach_counter = coach_counter + 1
    
    return coach_data
