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

def convert(coaches, locations, programs):
    # excel_file = request.files['file']
    current_date = datetime.date(2023,11,19)
    num_simulations=3

    # Read each sheet into a DataFrame
    df_coaches_profile = pd.DataFrame(coaches)
    df_locations_profile = pd.DataFrame(locations)
    df_programs_schedule = pd.DataFrame(programs)
    print('Boom')
    final_df_org = process_data2(df_programs_schedule, df_locations_profile, df_coaches_profile)
    final_df = final_df_org.copy(deep=True)
    coachid_to_name = df_coaches_profile.set_index('coach_id')['coach_name'].to_dict()
    name_to_coachid = df_coaches_profile.set_index('coach_name')['coach_id'].to_dict()

    final_df['assigned_coach']=final_df['assigned_coach'].apply(convert_coach_name)
    final_df['assigned_coach'] = final_df['assigned_coach'].apply(lambda names: [replace_names_with_ids(name, name_to_coachid) for name in names] if not pd.isnull(names) else None)

    df_past_programs = final_df.loc[final_df['dates']<pd.to_datetime(str(current_date))]
    # df_past_programs['Coach ID'] = df_past_programs['Ref Coach']df_curr_day_programs_original = final_df[final_df['Dates']==str(current_date)]
    
    df_curr_day_programs_original = final_df[final_df['dates']==str(current_date)]
    # df_curr_day_programs_original['Coach ID'] = df_curr_day_programs_original.apply(lambda row: get_latest_coach(row, df_past_programs,name_to_coachid), axis=1)
    
    #CUSTOM ALGORTIHM START

    simulations=[]
    df_curr_day_programs = df_curr_day_programs_original.sort_values(by=['school','start_time']).copy(deep=True)
    best_input = df_curr_day_programs.copy(deep=True)
    df_curr_day_programs['Second Filtered Head Coaches'] = None
    df_curr_day_programs['Time to Reach'] = None
    df_curr_day_programs['Travel Time for Suggested Coach'] = 0
    df_curr_day_programs['Total Time'] = 0

    grouped = df_curr_day_programs.groupby('assigned_coach')
    coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
    coaches_curr_day_busy_schedule_dict = coaches_curr_day_busy_schedule.to_dict() if not coaches_curr_day_busy_schedule.empty else {}
    travel_times = {coach: sum(calculate_travel_time_in_minutes((start_event.latitude,start_event.longitude), (end_event.latitude,end_event.longitude)) for start_event, end_event in get_travel_segments(events)) for coach, events in coaches_curr_day_busy_schedule_dict.items()}
    travel_times_to_first_event = {coach: get_travel_time_to_first_event(coach, coaches_curr_day_busy_schedule_dict, df_coaches_profile) for coach in coaches_curr_day_busy_schedule_dict.keys()}
    coach_travel_time_dict = {coach: (travel_times.get(coach, 0) or 0) + (travel_times_to_first_event.get(coach, 0) or 0) for coach in set(travel_times) | set(travel_times_to_first_event)}
    curr_job_time = (df_curr_day_programs.groupby('assigned_coach')['job_time'].sum())
    coach_job_time_dict = curr_job_time.to_dict()
    coach_total_time_dict = {coach: travel_time + job_time for coach, travel_time, job_time in zip(coach_travel_time_dict.keys(), coach_travel_time_dict.values(), coach_job_time_dict.values())}

    for index,row in df_curr_day_programs.iterrows():
        if not pd.isnull(row['assigned_coach']):
            continue
        # print('Balle')
        second_filtered_coaches_curr_program = []
        times_to_reach_curr_program = []
        grouped = df_curr_day_programs.groupby('assigned_coach')
        coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
        df_coaches_total_minutes = df_curr_day_programs.groupby('assigned_coach')['Total Time'].sum()
        preferred_coaches_curr_program = row['filtered_head_coaches']
        for coach in preferred_coaches_curr_program:
            if coach_total_time_dict.get(coach, 0)>(int(df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'work_hours'].iloc[0])-1)*60:
                continue
            coach_schedule = coaches_curr_day_busy_schedule.get(coach, None)
            if coach_schedule is None:
                second_filtered_coaches_curr_program.append(coach)
                last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                times_to_reach_curr_program.append(travel_time_to_reach)
            else:
                overlapping_time_windows = [tw for tw in coach_schedule if tw.start_time < row['end_time'] and row['start_time'] < tw.end_time]
                if len(overlapping_time_windows)>0:
                    continue
                non_overlapping_time_windows = [tw for tw in coach_schedule if not (tw in overlapping_time_windows)]
                start_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['start_time'])
                end_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['end_time'])
                # Any Program before the current program that has been completed
                time_window_before = min((tw for tw in non_overlapping_time_windows if tw.end_time <= row['start_time']), default=None, key=lambda tw: (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), tw.end_time)).total_seconds())
                time_window_after = min((tw for tw in non_overlapping_time_windows if tw.start_time >= row['end_time']), default=None, key=lambda tw: (datetime.datetime.combine(datetime.datetime.today(), tw.start_time) - end_time_datetime).total_seconds())
                if time_window_before:
                    if time_window_after:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach and available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                else:
                    if time_window_after:
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                            last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        second_filtered_coaches_curr_program.append(coach)
                        last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                        last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                        times_to_reach_curr_program.append(travel_time_to_reach)
        sorted_coaches_times_to_reach = sorted(zip(second_filtered_coaches_curr_program, times_to_reach_curr_program), key=lambda x: x[1])

        if sorted_coaches_times_to_reach:
            sorted_coaches, sorted_times_to_reach = zip(*sorted_coaches_times_to_reach)
        else:
            # print(index)
            sorted_coaches, sorted_times_to_reach = [], []
        
        df_curr_day_programs.loc[index, 'Second Filtered Head Coaches'] = ','.join(sorted_coaches)
        df_curr_day_programs.loc[index, 'Time to Reach'] = ','.join(map(str, sorted_times_to_reach))
        df_curr_day_programs.loc[index, 'assigned_coach'] = sorted_coaches[0] if len(sorted_coaches)>0 else None
        df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach'] = sorted_times_to_reach[0] if len(sorted_times_to_reach)>0 else 0
        df_curr_day_programs.loc[index, 'Total Time'] = (df_curr_day_programs.loc[index, 'job_time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']) if len(sorted_times_to_reach)>0 else 0
        if df_curr_day_programs.loc[index, 'assigned_coach']:
            coach_id = df_curr_day_programs.loc[index, 'assigned_coach']
            coach_travel_time_dict[coach_id] = coach_travel_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
            coach_job_time_dict[coach_id] = coach_job_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'job_time']
            coach_total_time_dict[coach_id] = coach_total_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'job_time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
    all_coaches_total_time = sum(coach_total_time_dict.values())
    all_coaches_travel_time = sum(coach_travel_time_dict.values())
    all_coaches_job_time = sum(coach_job_time_dict.values())

    new_simulation = {'total_job_time': all_coaches_job_time, 'total_travel_time': all_coaches_travel_time,'input':best_input}
    simulations.append(new_simulation)

    for i in range(num_simulations):
        groups = [df for _, df in df_curr_day_programs_original.groupby('school')]
        random.shuffle(groups)
        df_curr_day_programs = pd.concat(groups).copy(deep=True)
        best_input = df_curr_day_programs.copy(deep=True)
        df_curr_day_programs['Second Filtered Head Coaches'] = None
        df_curr_day_programs['Time to Reach'] = None
        df_curr_day_programs['Travel Time for Suggested Coach'] = 0
        df_curr_day_programs['Total Time'] = 0

        grouped = df_curr_day_programs.groupby('assigned_coach')
        coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
        coaches_curr_day_busy_schedule_dict = coaches_curr_day_busy_schedule.to_dict() if not coaches_curr_day_busy_schedule.empty else {}
        travel_times = {coach: sum(calculate_travel_time_in_minutes((start_event.latitude,start_event.longitude), (end_event.latitude,end_event.longitude)) for start_event, end_event in get_travel_segments(events)) for coach, events in coaches_curr_day_busy_schedule_dict.items()}
        travel_times_to_first_event = {coach: get_travel_time_to_first_event(coach, coaches_curr_day_busy_schedule_dict, df_coaches_profile) for coach in coaches_curr_day_busy_schedule_dict.keys()}
        coach_travel_time_dict = {coach: (travel_times.get(coach, 0) or 0) + (travel_times_to_first_event.get(coach, 0) or 0) for coach in set(travel_times) | set(travel_times_to_first_event)}
        curr_job_time = (df_curr_day_programs.groupby('assigned_coach')['job_time'].sum())
        coach_job_time_dict = curr_job_time.to_dict()
        coach_total_time_dict = {coach: travel_time + job_time for coach, travel_time, job_time in zip(coach_travel_time_dict.keys(), coach_travel_time_dict.values(), coach_job_time_dict.values())}

        for index,row in df_curr_day_programs.iterrows():
            if not pd.isnull(row['assigned_coach']):
                continue
            second_filtered_coaches_curr_program = []
            times_to_reach_curr_program = []
            grouped = df_curr_day_programs.groupby('assigned_coach')
            coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
            df_coaches_total_minutes = df_curr_day_programs.groupby('assigned_coach')['Total Time'].sum()
            preferred_coaches_curr_program = row['filtered_head_coaches']
            for coach in preferred_coaches_curr_program:
                if coach_total_time_dict.get(coach, 0)>(int(df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'work_hours'].iloc[0])-1)*60:
                    continue
                coach_schedule = coaches_curr_day_busy_schedule.get(coach, None)
                if coach_schedule is None:
                    second_filtered_coaches_curr_program.append(coach)
                    last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                    last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                    travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                    times_to_reach_curr_program.append(travel_time_to_reach)
                else:
                    overlapping_time_windows = [tw for tw in coach_schedule if tw.start_time < row['end_time'] and row['start_time'] < tw.end_time]
                    if len(overlapping_time_windows)>0:
                        continue
                    non_overlapping_time_windows = [tw for tw in coach_schedule if not (tw in overlapping_time_windows)]
                    start_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['start_time'])
                    end_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['end_time'])
                    # Any Program before the current program that has been completed
                    time_window_before = min((tw for tw in non_overlapping_time_windows if tw.end_time <= row['start_time']), default=None, key=lambda tw: (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), tw.end_time)).total_seconds())
                    time_window_after = min((tw for tw in non_overlapping_time_windows if tw.start_time >= row['end_time']), default=None, key=lambda tw: (datetime.datetime.combine(datetime.datetime.today(), tw.start_time) - end_time_datetime).total_seconds())
                    if time_window_before:
                        if time_window_after:
                            last_location_lat = time_window_before.latitude
                            last_location_lon = time_window_before.longitude
                            next_location_lat = time_window_after.latitude
                            next_location_lon = time_window_after.longitude
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                            travel_time_to_depart = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (next_location_lat, next_location_lon)))
                            available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                            available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                            if available_time_to_reach >= travel_time_to_reach and available_time_to_depart>=travel_time_to_depart:
                                second_filtered_coaches_curr_program.append(coach)
                                times_to_reach_curr_program.append(travel_time_to_reach)
                        else:
                            last_location_lat = time_window_before.latitude
                            last_location_lon = time_window_before.longitude
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                            available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                            if available_time_to_reach >= travel_time_to_reach:
                                second_filtered_coaches_curr_program.append(coach)
                                times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        if time_window_after:
                            next_location_lat = time_window_after.latitude
                            next_location_lon = time_window_after.longitude
                            travel_time_to_depart = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (next_location_lat, next_location_lon)))
                            available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                            if available_time_to_depart>=travel_time_to_depart:
                                second_filtered_coaches_curr_program.append(coach)
                                last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                                last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                                travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                                times_to_reach_curr_program.append(travel_time_to_reach)
                        else:
                            second_filtered_coaches_curr_program.append(coach)
                            last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                            last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                            times_to_reach_curr_program.append(travel_time_to_reach)
            sorted_coaches_times_to_reach = sorted(zip(second_filtered_coaches_curr_program, times_to_reach_curr_program), key=lambda x: x[1])

            if sorted_coaches_times_to_reach:
                sorted_coaches, sorted_times_to_reach = zip(*sorted_coaches_times_to_reach)
            else:
                sorted_coaches, sorted_times_to_reach = [], []
            df_curr_day_programs.loc[index, 'Second Filtered Head Coaches'] = ','.join(sorted_coaches)
            df_curr_day_programs.loc[index, 'Time to Reach'] = ','.join(map(str, sorted_times_to_reach))
            df_curr_day_programs.loc[index, 'assigned_coach'] = sorted_coaches[0] if len(sorted_coaches)>0 else None
            df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach'] = sorted_times_to_reach[0] if len(sorted_times_to_reach)>0 else 0
            df_curr_day_programs.loc[index, 'Total Time'] = (df_curr_day_programs.loc[index, 'job_time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']) if len(sorted_times_to_reach)>0 else 0
            if df_curr_day_programs.loc[index, 'assigned_coach']:
                coach_id = df_curr_day_programs.loc[index, 'assigned_coach']
                coach_travel_time_dict[coach_id] = coach_travel_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
                coach_job_time_dict[coach_id] = coach_job_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'job_time']
                coach_total_time_dict[coach_id] = coach_total_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'job_time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
        all_coaches_total_time = sum(coach_total_time_dict.values())
        all_coaches_travel_time = sum(coach_travel_time_dict.values())
        all_coaches_job_time = sum(coach_job_time_dict.values())

        new_simulation = {'total_job_time': all_coaches_job_time, 'total_travel_time': all_coaches_travel_time,'input':best_input}
        simulations.append(new_simulation)
    selected_simulation = max(simulations, key=lambda x: (x['total_job_time']-x['total_travel_time']))

    curr_best = selected_simulation['input'].copy(deep=True)
    df_curr_day_programs = curr_best.copy(deep=True)
    df_curr_day_programs['Second Filtered Head Coaches'] = None
    df_curr_day_programs['Time to Reach'] = None
    df_curr_day_programs['Travel Time for Suggested Coach'] = 0
    df_curr_day_programs['Total Time'] = 0

    grouped = df_curr_day_programs.groupby('assigned_coach')
    coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
    coaches_curr_day_busy_schedule_dict = coaches_curr_day_busy_schedule.to_dict() if not coaches_curr_day_busy_schedule.empty else {}
    travel_times = {coach: sum(calculate_travel_time_in_minutes((start_event.latitude,start_event.longitude), (end_event.latitude,end_event.longitude)) for start_event, end_event in get_travel_segments(events)) for coach, events in coaches_curr_day_busy_schedule_dict.items()}
    travel_times_to_first_event = {coach: get_travel_time_to_first_event(coach, coaches_curr_day_busy_schedule_dict, df_coaches_profile) for coach in coaches_curr_day_busy_schedule_dict.keys()}
    coach_travel_time_dict = {coach: (travel_times.get(coach, 0) or 0) + (travel_times_to_first_event.get(coach, 0) or 0) for coach in set(travel_times) | set(travel_times_to_first_event)}
    curr_job_time = (df_curr_day_programs.groupby('assigned_coach')['job_time'].sum())
    coach_job_time_dict = curr_job_time.to_dict()
    coach_total_time_dict = {coach: travel_time + job_time for coach, travel_time, job_time in zip(coach_travel_time_dict.keys(), coach_travel_time_dict.values(), coach_job_time_dict.values())}

    for index,row in df_curr_day_programs.iterrows():
        if not pd.isnull(row['assigned_coach']):
            continue
        second_filtered_coaches_curr_program = []
        times_to_reach_curr_program = []
        grouped = df_curr_day_programs.groupby('assigned_coach')
        coaches_curr_day_busy_schedule = grouped.apply(lambda row: sorted([Event('Program',start,end,lat,lon,loc_acr,court_loc) for start, end, lat,lon,loc_acr,court_loc in get_event_time_location(row)], key=lambda x: x.end_time))
        df_coaches_total_minutes = df_curr_day_programs.groupby('assigned_coach')['Total Time'].sum()
        preferred_coaches_curr_program = row['filtered_head_coaches']
        for coach in preferred_coaches_curr_program:
            if coach_total_time_dict.get(coach, 0)>(int(df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'work_hours'].iloc[0])-1)*60:
                continue
            coach_schedule = coaches_curr_day_busy_schedule.get(coach, None)
            if coach_schedule is None:
                second_filtered_coaches_curr_program.append(coach)
                last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                times_to_reach_curr_program.append(travel_time_to_reach)
            else:
                overlapping_time_windows = [tw for tw in coach_schedule if tw.start_time < row['end_time'] and row['start_time'] < tw.end_time]
                if len(overlapping_time_windows)>0:
                    continue
                non_overlapping_time_windows = [tw for tw in coach_schedule if not (tw in overlapping_time_windows)]
                start_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['start_time'])
                end_time_datetime = datetime.datetime.combine(datetime.datetime.today(), row['end_time'])
                # Any Program before the current program that has been completed
                time_window_before = min((tw for tw in non_overlapping_time_windows if tw.end_time <= row['start_time']), default=None, key=lambda tw: (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), tw.end_time)).total_seconds())
                time_window_after = min((tw for tw in non_overlapping_time_windows if tw.start_time >= row['end_time']), default=None, key=lambda tw: (datetime.datetime.combine(datetime.datetime.today(), tw.start_time) - end_time_datetime).total_seconds())
                if time_window_before:
                    if time_window_after:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach and available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        last_location_lat = time_window_before.latitude
                        last_location_lon = time_window_before.longitude
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                        available_time_to_reach = (start_time_datetime - datetime.datetime.combine(datetime.datetime.today(), time_window_before.end_time)).total_seconds() / 60
                        if available_time_to_reach >= travel_time_to_reach:
                            second_filtered_coaches_curr_program.append(coach)
                            times_to_reach_curr_program.append(travel_time_to_reach)
                else:
                    if time_window_after:
                        next_location_lat = time_window_after.latitude
                        next_location_lon = time_window_after.longitude
                        travel_time_to_depart = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (next_location_lat, next_location_lon)))
                        available_time_to_depart = (datetime.datetime.combine(datetime.datetime.today(), time_window_after.start_time) - end_time_datetime ).total_seconds() / 60
                        if available_time_to_depart>=travel_time_to_depart:
                            second_filtered_coaches_curr_program.append(coach)
                            last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                            last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                            travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                            times_to_reach_curr_program.append(travel_time_to_reach)
                    else:
                        second_filtered_coaches_curr_program.append(coach)
                        last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
                        last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_long'].iloc[0]
                        travel_time_to_reach = int(calculate_travel_time_in_minutes((row['latitude'],row['longitude']), (last_location_lat, last_location_lon)))
                        times_to_reach_curr_program.append(travel_time_to_reach)
        sorted_coaches_times_to_reach = sorted(zip(second_filtered_coaches_curr_program, times_to_reach_curr_program), key=lambda x: x[1])

        if sorted_coaches_times_to_reach:
            sorted_coaches, sorted_times_to_reach = zip(*sorted_coaches_times_to_reach)
        else:
            print(index)
            sorted_coaches, sorted_times_to_reach = [], []
        
        df_curr_day_programs.loc[index, 'Second Filtered Head Coaches'] = ','.join(sorted_coaches)
        df_curr_day_programs.loc[index, 'Time to Reach'] = ','.join(map(str, sorted_times_to_reach))
        df_curr_day_programs.loc[index, 'assigned_coach'] = sorted_coaches[0] if len(sorted_coaches)>0 else None
        df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach'] = sorted_times_to_reach[0] if len(sorted_times_to_reach)>0 else 0
        df_curr_day_programs.loc[index, 'Total Time'] = (df_curr_day_programs.loc[index, 'job_time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']) if len(sorted_times_to_reach)>0 else 0
        if df_curr_day_programs.loc[index, 'assigned_coach']:
            coach_id = df_curr_day_programs.loc[index, 'assigned_coach']
            coach_travel_time_dict[coach_id] = coach_travel_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
            coach_job_time_dict[coach_id] = coach_job_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'job_time']
            coach_total_time_dict[coach_id] = coach_total_time_dict.get(coach_id, 0) + df_curr_day_programs.loc[index, 'job_time'] + df_curr_day_programs.loc[index, 'Travel Time for Suggested Coach']
    all_coaches_total_time = sum(coach_total_time_dict.values())
    all_coaches_travel_time = sum(coach_travel_time_dict.values())
    all_coaches_job_time = sum(coach_job_time_dict.values())

    output_csv = df_curr_day_programs.to_csv(index=False)

    return output_csv