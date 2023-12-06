import random
import datetime

from .helper_functions import *
import warnings
warnings.filterwarnings('ignore')

class Event:
    def __init__(self, type, start_time, end_time,latitude,longitude,location_acronym,court_location):
        self.type = type
        self.location_acronym = location_acronym
        self.court_location = court_location
        self.latitude = latitude
        self.longitude = longitude
        self.start_time = start_time
        self.end_time = end_time

def get_event_time_location(group):
    event = list(zip(group['Start Time'], group['End Time'],group['Latitude'],group['Longitude'],group['Location Acronym'],group['Court Location Abbreviation']))
    return event

def convert(file):
    # excel_file = request.files['file']
    current_date = datetime.date(2023,11,19)
    num_simulations=3
    xls = pd.ExcelFile(file)

    # Read each sheet into a DataFrame
    df_coaches_profile = pd.read_excel(xls, 'Coaches', index_col=None)
    df_programs_schedule = pd.read_excel(xls, 'Programs', index_col=None)
    df_locations_profile = pd.read_excel(xls, 'Locations', index_col=None)
    print('Boom')
    final_df_org = process_data(df_programs_schedule, df_locations_profile, df_coaches_profile)
    final_df = final_df_org.copy(deep=True)

    coachid_to_name = df_coaches_profile.set_index('Coach ID')['Coach Name'].to_dict()
    name_to_coachid = df_coaches_profile.set_index('Coach Name')['Coach ID'].to_dict()

    final_df['Coach ID']=final_df['Coach'].apply(convert_coach_name)
    final_df['Coach ID']=final_df['Coach ID'].apply(lambda names: ','.join(replace_names_with_ids(name,name_to_coachid) for name in names.split(',')))
    final_df=final_df.drop(columns=['Coach'])
    final_df['Ref Coach']=final_df['Coach ID']
    final_df['Coach ID']=None
    df_past_programs = final_df.loc[final_df['Dates']<pd.to_datetime(str(current_date))]
    df_curr_day_programs = final_df[final_df['Dates']==str(current_date)]

    df_curr_day_programs['Coach ID'] = df_curr_day_programs.apply(lambda row: get_latest_coach(row, df_past_programs,name_to_coachid), axis=1)
    # grouped = df_curr_day_programs.groupby('Coach ID')
    # coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))

    #CUSTOM ALGORTIHM START
    df_past_programs = final_df.loc[final_df['Dates']<pd.to_datetime(str(current_date))]
    df_curr_day_programs_original = final_df[final_df['Dates']==str(current_date)]

    simulations=[]
    df_curr_day_programs = df_curr_day_programs_original.sort_values(by=['Location Acronym','Start Time']).copy(deep=True)
    best_input = df_curr_day_programs.copy(deep=True)
    df_curr_day_programs['Second Filtered Head Coaches'] = None
    df_curr_day_programs['Time to Reach'] = None
    df_curr_day_programs['Travel Time for Suggested Coach'] = 0
    df_curr_day_programs['Total Time'] = 0

    coach_travel_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}
    coach_job_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}
    coach_total_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}

    for index,row in df_curr_day_programs.iterrows():
        second_filtered_coaches_curr_program = []
        times_to_reach_curr_program = []
        grouped = df_curr_day_programs.groupby('Coach ID')
        coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
        df_coaches_total_minutes = df_curr_day_programs.groupby('Coach ID')['Total Time'].sum()
        preferred_coaches_curr_program = row['Filtered Head Coaches'].split(',')
        for coach in preferred_coaches_curr_program:
            if coach_total_time_dict.get(coach, 0)>(int(df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Hours of work'].iloc[0])-1)*60:
                continue
            coach_schedule = coaches_curr_day_busy_schedule.get(coach, None)
            if coach_schedule is None:
                second_filtered_coaches_curr_program.append(coach)
                last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                times_to_reach_curr_program.append(travel_time_to_reach)
            else:
                overlapping_time_windows = [tw for tw in coach_schedule if tw.start_time < row['End Time'] and row['Start Time'] < tw.end_time]
                if len(overlapping_time_windows)>0:
                    continue
                non_overlapping_time_windows = [tw for tw in coach_schedule if not (tw in overlapping_time_windows)]
                start_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['Start Time'])
                end_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['End Time'])
                # Any Program before the current program that has been completed
                time_window_before = min((tw for tw in non_overlapping_time_windows if tw.end_time <= row['Start Time']), default=None, key=lambda tw: (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), tw.end_time)).total_seconds())
                time_window_after = min((tw for tw in non_overlapping_time_windows if tw.start_time >= row['End Time']), default=None, key=lambda tw: (datetime.datetime.combine(datetime.datetime.today(), tw.start_time) - end_time_datetime).total_seconds())
                if time_window_before:
                    if time_window_after:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach and available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                        
                    # print(coach,'C',second_filtered_coaches_curr_program,times_to_reach_curr_program)
                else:
                    if time_window_after:
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                            last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        second_filtered_coaches_curr_program.append(coach)
                        last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                        last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                        times_to_reach_curr_program.append(travel_time_to_reach)
                    # print(coach,'D',second_filtered_coaches_curr_program,times_to_reach_curr_program)            
        sorted_coaches_times_to_reach = sorted(zip(second_filtered_coaches_curr_program, times_to_reach_curr_program), key=lambda x: x[1])

        if sorted_coaches_times_to_reach:
            sorted_coaches, sorted_times_to_reach = zip(*sorted_coaches_times_to_reach)
        else:
            # print(index)
            sorted_coaches, sorted_times_to_reach = [], []
        
        df_curr_day_programs.loc[index, 'Second Filtered Head Coaches'] = ','.join(sorted_coaches)
        df_curr_day_programs.loc[index, 'Time to Reach'] = ','.join(map(str, sorted_times_to_reach))
        df_curr_day_programs.loc[index, 'Coach ID'] = sorted_coaches[0] if len(sorted_coaches)>0 else None
        df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach'] = sorted_times_to_reach[0] if len(sorted_times_to_reach)>0 else 0
        df_curr_day_programs.loc[index, 'Total Time'] = (df_curr_day_programs.loc[index, 'Job Time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']) if len(sorted_times_to_reach)>0 else 0
        if df_curr_day_programs.loc[index, 'Coach ID']:
            coach_id = df_curr_day_programs.loc[index, 'Coach ID']
            coach_travel_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
            coach_job_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Job Time']
            coach_total_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Job Time']+df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
        # if count==10:
        #     break
        # count+=1
    all_coaches_total_time = sum(coach_total_time_dict.values())
    all_coaches_travel_time = sum(coach_travel_time_dict.values())
    all_coaches_job_time = sum(coach_job_time_dict.values())

    new_simulation = {'total_job_time': all_coaches_job_time, 'total_travel_time': all_coaches_travel_time,'input':best_input}
    simulations.append(new_simulation)

    for i in range(num_simulations):
        groups = [df for _, df in df_curr_day_programs_original.groupby('Location Acronym')]
        random.shuffle(groups)
        df_curr_day_programs = pd.concat(groups).copy(deep=True)
        best_input = df_curr_day_programs.copy(deep=True)
        df_curr_day_programs['Second Filtered Head Coaches'] = None
        df_curr_day_programs['Time to Reach'] = None
        df_curr_day_programs['Travel Time for Suggested Coach'] = 0
        df_curr_day_programs['Total Time'] = 0

        coach_travel_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}
        coach_job_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}
        coach_total_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}

        for index,row in df_curr_day_programs.iterrows():
            second_filtered_coaches_curr_program = []
            times_to_reach_curr_program = []
            grouped = df_curr_day_programs.groupby('Coach ID')
            coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
            df_coaches_total_minutes = df_curr_day_programs.groupby('Coach ID')['Total Time'].sum()
            preferred_coaches_curr_program = row['Filtered Head Coaches'].split(',')
            for coach in preferred_coaches_curr_program:
                if coach_total_time_dict.get(coach, 0)>(int(df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Hours of work'].iloc[0])-1)*60:
                    continue
                coach_schedule = coaches_curr_day_busy_schedule.get(coach, None)
                if coach_schedule is None:
                    second_filtered_coaches_curr_program.append(coach)
                    last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                    last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                    travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                    times_to_reach_curr_program.append(travel_time_to_reach)
                else:
                    overlapping_time_windows = [tw for tw in coach_schedule if tw.start_time < row['End Time'] and row['Start Time'] < tw.end_time]
                    if len(overlapping_time_windows)>0:
                        continue
                    non_overlapping_time_windows = [tw for tw in coach_schedule if not (tw in overlapping_time_windows)]
                    start_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['Start Time'])
                    # Any Program before the current program that has been completed
                    time_window_before = min((tw for tw in non_overlapping_time_windows if tw.end_time <= row['Start Time']), default=None, key=lambda tw: (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), tw.end_time)).total_seconds())
                    time_window_after = min((tw for tw in non_overlapping_time_windows if tw.start_time >= row['End Time']), default=None, key=lambda tw: (datetime.datetime.combine(datetime.datetime.today(), tw.start_time) - end_time_datetime).total_seconds())
                    if time_window_before:
                        if time_window_after:
                            last_location_lat = time_window_before.latitude
                            last_location_lon = time_window_before.longitude
                            next_location_lat = time_window_after.latitude
                            next_location_lon = time_window_after.longitude
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                            travel_time_to_depart = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (next_location_lat, next_location_lon)))
                            available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                            available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                            if available_time_to_reach >= travel_time_to_reach and available_time_to_depart>=travel_time_to_depart:
                                second_filtered_coaches_curr_program.append(coach)
                                times_to_reach_curr_program.append(travel_time_to_reach)
                        else:
                            last_location_lat = time_window_before.latitude
                            last_location_lon = time_window_before.longitude
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                            available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                            if available_time_to_reach >= travel_time_to_reach:
                                second_filtered_coaches_curr_program.append(coach)
                                times_to_reach_curr_program.append(travel_time_to_reach)
                            
                        # print(coach,'C',second_filtered_coaches_curr_program,times_to_reach_curr_program)
                    else:
                        if time_window_after:
                            next_location_lat = time_window_after.latitude
                            next_location_lon = time_window_after.longitude
                            travel_time_to_depart = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (next_location_lat, next_location_lon)))
                            available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                            if available_time_to_depart>=travel_time_to_depart:
                                second_filtered_coaches_curr_program.append(coach)
                                last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                                last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                                travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                                times_to_reach_curr_program.append(travel_time_to_reach)
                        else:
                            second_filtered_coaches_curr_program.append(coach)
                            last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                            last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                            times_to_reach_curr_program.append(travel_time_to_reach)
                        # print(coach,'D',second_filtered_coaches_curr_program,times_to_reach_curr_program)            
            sorted_coaches_times_to_reach = sorted(zip(second_filtered_coaches_curr_program, times_to_reach_curr_program), key=lambda x: x[1])

            if sorted_coaches_times_to_reach:
                sorted_coaches, sorted_times_to_reach = zip(*sorted_coaches_times_to_reach)
            else:
                # print(index)
                sorted_coaches, sorted_times_to_reach = [], []
            
            df_curr_day_programs.loc[index, 'Second Filtered Head Coaches'] = ','.join(sorted_coaches)
            df_curr_day_programs.loc[index, 'Time to Reach'] = ','.join(map(str, sorted_times_to_reach))
            df_curr_day_programs.loc[index, 'Coach ID'] = sorted_coaches[0] if len(sorted_coaches)>0 else None
            df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach'] = sorted_times_to_reach[0] if len(sorted_times_to_reach)>0 else 0
            df_curr_day_programs.loc[index, 'Total Time'] = (df_curr_day_programs.loc[index, 'Job Time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']) if len(sorted_times_to_reach)>0 else 0
            if df_curr_day_programs.loc[index, 'Coach ID']:
                coach_id = df_curr_day_programs.loc[index, 'Coach ID']
                coach_travel_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
                coach_job_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Job Time']
                coach_total_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Job Time']+df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
            # if count==10:
            #     break
            # count+=1
        all_coaches_total_time = sum(coach_total_time_dict.values())
        all_coaches_travel_time = sum(coach_travel_time_dict.values())
        all_coaches_job_time = sum(coach_job_time_dict.values())

        new_simulation = {'total_job_time': all_coaches_job_time, 'total_travel_time': all_coaches_travel_time,'input':best_input}
        simulations.append(new_simulation)

    selected_simulation = max(simulations, key=lambda x: (x['total_job_time'],-x['total_travel_time']))

    curr_best = selected_simulation['input'].copy(deep=True)
    df_curr_day_programs = curr_best.copy(deep=True)
    df_curr_day_programs['Second Filtered Head Coaches'] = None
    df_curr_day_programs['Time to Reach'] = None
    df_curr_day_programs['Travel Time for Suggested Coach'] = 0
    df_curr_day_programs['Total Time'] = 0

    coach_travel_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}
    coach_job_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}
    coach_total_time_dict = {coach_id: 0 for coach_id in df_coaches_profile['Coach ID']}

    for index,row in df_curr_day_programs.iterrows():
        second_filtered_coaches_curr_program = []
        times_to_reach_curr_program = []
        #Get coach's busy schedule of programs
        grouped = df_curr_day_programs.groupby('Coach ID')
        coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
        df_coaches_total_minutes = df_curr_day_programs.groupby('Coach ID')['Total Time'].sum()
        preferred_coaches_curr_program = row['Filtered Head Coaches'].split(',')
        # random.shuffle(preferred_coaches_curr_program)
        for coach in preferred_coaches_curr_program:
            if coach_total_time_dict.get(coach, 0)>(int(df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Hours of work'].iloc[0])-1)*60:
                continue
            # print(coach,'A')
            coach_schedule = coaches_curr_day_busy_schedule.get(coach, None)
            if coach_schedule is None:
                second_filtered_coaches_curr_program.append(coach)
                last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                times_to_reach_curr_program.append(travel_time_to_reach)

            else:
                overlapping_time_windows = [tw for tw in coach_schedule if tw.start_time < row['End Time'] and row['Start Time'] < tw.end_time]
                if len(overlapping_time_windows)>0:
                    continue
                non_overlapping_time_windows = [tw for tw in coach_schedule if not (tw in overlapping_time_windows)]
                start_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['Start Time'])
                # Any Program before the current program that has been completed
                time_window_before = min((tw for tw in non_overlapping_time_windows if tw.end_time <= row['Start Time']), default=None, key=lambda tw: (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), tw.end_time)).total_seconds())
                time_window_after = min((tw for tw in non_overlapping_time_windows if tw.start_time >= row['End Time']), default=None, key=lambda tw: (datetime.datetime.combine(datetime.datetime.today(), tw.start_time) - end_time_datetime).total_seconds())
                if time_window_before:
                    if time_window_after:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach and available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                else:
                    if time_window_after:
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                            last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        second_filtered_coaches_curr_program.append(coach)
                        last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
                        last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['Latitude'],row['Longitude']), (last_location_lat, last_location_lon)))
                        times_to_reach_curr_program.append(travel_time_to_reach)          
        sorted_coaches_times_to_reach = sorted(zip(second_filtered_coaches_curr_program, times_to_reach_curr_program), key=lambda x: x[1])

        if sorted_coaches_times_to_reach:
            sorted_coaches, sorted_times_to_reach = zip(*sorted_coaches_times_to_reach)
        else:
            print(index)
            sorted_coaches, sorted_times_to_reach = [], []
        
        df_curr_day_programs.loc[index, 'Second Filtered Head Coaches'] = ','.join(sorted_coaches)
        df_curr_day_programs.loc[index, 'Time to Reach'] = ','.join(map(str, sorted_times_to_reach))
        df_curr_day_programs.loc[index, 'Coach ID'] = sorted_coaches[0] if len(sorted_coaches)>0 else None
        df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach'] = sorted_times_to_reach[0] if len(sorted_times_to_reach)>0 else 0
        df_curr_day_programs.loc[index, 'Total Time'] = (df_curr_day_programs.loc[index, 'Job Time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']) if len(sorted_times_to_reach)>0 else 0
        if df_curr_day_programs.loc[index, 'Coach ID']:
            coach_id = df_curr_day_programs.loc[index, 'Coach ID']
            coach_travel_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
            coach_job_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Job Time']
            coach_total_time_dict[coach_id] += df_curr_day_programs.loc[index, 'Job Time']+df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']

    all_coaches_total_time = sum(coach_total_time_dict.values())
    all_coaches_travel_time = sum(coach_travel_time_dict.values())
    all_coaches_job_time = sum(coach_job_time_dict.values())
    output_csv = df_curr_day_programs.to_csv(index=False)

    return output_csv