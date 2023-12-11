import pandas as pd
import sys, os, copy
import requests, json
import urllib.request
import ast

import datetime
import numpy as np
from haversine import haversine
from scipy.spatial.distance import cdist

def process_programs_schedule(df_programs_schedule):
    df_programs_schedule = df_programs_schedule.copy(deep=True)
    df_programs_schedule['Start Date'] = pd.to_datetime(df_programs_schedule['Start Date'],format='%d-%m-%Y')
    df_programs_schedule['End Date'] = pd.to_datetime(df_programs_schedule['End Date'],format='%d-%m-%Y')
    df_programs_schedule['Date does not have a sessions'] = df_programs_schedule['Date does not have a sessions'].apply(lambda x: pd.to_datetime([date.strip() for date in x.split(',')], format='%d-%m-%Y') if pd.notnull(x) else [])
    ### If ABOVE DOESNT WORK THEN PREPROCESSING REQUIRED IN PROGRAMS_SCHEDULE FILE
    # df_programs_schedule['Start Date'] = pd.to_datetime(df_programs_schedule['Start Date'])
    # df_programs_schedule['End Date'] = df_programs_schedule['Start Date'] + pd.to_timedelta(df_programs_schedule['Weeks']*7, unit='d')
    # df_programs_schedule['Start Date'] = df_programs_schedule['Start Date'].dt.strftime('%d-%m-%Y').astype(str) # Use this at the time of saving the csv for Readability
    # df_programs_schedule['End Date'] = df_programs_schedule['End Date'].dt.strftime('%d-%m-%Y').astype(str) # Use this at the time of saving the csv for Readability
    # df_programs_schedule.to_csv(programs_schedule_file_path, index=False)
    df_programs_schedule['Dates'] = df_programs_schedule.apply(lambda row: pd.date_range(start=row['Start Date'], end=row['End Date']).difference(row['Date does not have a sessions']), axis=1)
    df_programs_schedule = df_programs_schedule.explode('Dates')
    df_programs = df_programs_schedule[df_programs_schedule.apply(lambda row: row['Dates'].strftime('%a') in [day.strip() for day in row['Days'].split(',')], axis=1)]
    df_programs = df_programs.reset_index(drop=True)
    return df_programs

def calculate_travel_time_in_minutes(loc1, loc2):
    locs = [loc1, loc2]
    # Compute the distance matrix only for the two locations
    dist_matrix = cdist(locs, locs, metric=haversine)
    dist_matrix = np.ceil(dist_matrix * 1.35).astype(int)  # Typecasting to int # PREVIOUSLY WAS 1.27
    # Compute the time matrix
    time_matrix = np.ceil(dist_matrix*1.13)     # taking average vehicle speed to be ~60/1.2 for a straight line traversal  
    time_matrix = time_matrix[0, 1]
    time_matrix = time_matrix if time_matrix <= 80 else int(time_matrix/1.3)
    if time_matrix>0:
        time_matrix+=30
    return time_matrix

def replace_names_with_ids(name,name_to_coachid):
   return name_to_coachid.get(name, name)

def convert_coach_name(coach_name):
    coach_names = {
        'Abdoulaye Diallo':'Abdoulaye Diallo',
        'Ahmed Adel':'Ahmed Abdel',
        'Amir Parvizi':'Amir Parvizi',
        'Annas Shema':'Shema Annas',
        'Bashar Alikairawan':'Bashar Alkairawan',
        'Bashar Alikairawan/Ahmed Adel':'Bashar Alkairawan,Ahmed Abdel',
        'Behn Joseph Balijon':'Behn Balijon',
        'Brian Kasumba':'Brian Kasumba',
        'Carl David Managuelod': 'Carl David Managuelod',
        'Charles Yap': 'Charles Yap',
        'Clinton Oduro': 'Clinton Oduro',
        'Dave Clinton Salas': 'Dave Clinton Salas',
        'Godfrey Odong': 'Godfrey Odong',
        'Godfrey Odong/Amir Parvizi': 'Godfrey Odong,Amir Parvizi',
        'Godfrey Odong/Brian Kasumba': 'Godfrey Odong,Brian Kasumba',
        'Jelili Alimi':'Jelili Alimi',
        'Jeremy Manguro':'Jeremy Manguro',
        'John Mark Castro':'John Mark Castro',
        'Joshua Bortei':'Joshua Bortei',
        'Kamsi':'Kamsi',
        'Lamine Ndiaye':'Lamine Ndgiye',
        'Lark Andrew Santos':'Lark Andrew Santos',
        'Majille Malijan':'Majille Majilan',
        'Majille Malijon':'Majille Majilan',
        'Murad Hesham':'Murad Hesham',
        'TBC':'TBC',
        'TBH':'TBH',
    }
    if coach_name in coach_names:
        return coach_names[coach_name]
    else:
        return coach_name

# def get_latest_coach(row,df_history,name_to_coachid):
#     if pd.isnull(row['Coach ID']):
#         program_rows = df_history[df_history['PID'] == row['PID']]
#         if program_rows.empty:
#             return None
#         else:
#             latest_row = program_rows.sort_values('Dates', ascending=False).iloc[0]
#             if pd.isnull(latest_row['Ref Coach']):
#                 return None
#             else:
#                 coach_id = latest_row['Ref Coach']
#                 return coach_id
#     else:
#         return row['Coach ID']

# def get_travel_segments(events):
#     return zip(events[:-1], events[1:])
# def get_home_location(coach,df_coaches_profile):
#     last_location_lat = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Latitude'].iloc[0]
#     last_location_lon = df_coaches_profile.loc[df_coaches_profile['Coach ID'] == coach, 'Home Longitude'].iloc[0]
#     return (last_location_lat, last_location_lon)
# def get_travel_time_to_first_event(coach,coaches_curr_day_busy_schedule_dict,df_coaches_profile):
#     if coach in ['TBH','TBC']:
#         # print('oye')
#         return None
#     home_location = get_home_location(coach,df_coaches_profile)
#     events = coaches_curr_day_busy_schedule_dict.get(coach, [])
#     if events:
#         first_event_location = events[0].latitude, events[0].longitude
#         return calculate_travel_time_in_minutes(home_location, first_event_location)
#     else:
#         return None

# def get_times(group):
#     # Combine start and end time into a tuple, and make a list of these
#     times = list(zip(group['Start Time'], group['End Time']))
#     return times
    
# def get_event_time_location(group):
#     event = list(zip(group['Start Time'], group['End Time'],group['Latitude'],group['Longitude'],group['Location Acronym'],group['Court Location Abbreviation']))
#     return event

def process_data(df_programs_schedule, df_locations_profile, df_coaches_profile):
    # Your code here
    df_programs = process_programs_schedule(df_programs_schedule)
    merged_df = df_programs.merge(df_locations_profile, left_on='Location Acronym', right_on='Code', how='left')
    all_columns_after_merge = ['PID','Location Acronym','Court Location Abbreviation','Latitude','Longitude','Dates','Start Time', 'End Time','Age Group','Seats Taken','Term','Documented/Undocumented','Coaches','Allowed Head Coaches','Allowed Assistant Coaches','Location Name', 'Court Location', 'Days', 'Time', 'Program','Coach', 'Level', 'Class Type', 'Seat Capacity', 'Available Seats', 'Start Date', 'End Date', 'Weeks', 'Date does not have a sessions', 'School', 'Location', 'Location Map', 'Provider', 'Code', 'Storage', 'Is our ball bag stored ', 'Current Coach at this Location']
    # imp_columns_after_merge = ['PID','Location Acronym','Court Location Abbreviation','Latitude','Longitude','Dates','Days','Start Time', 'End Time','Age Group','Level','Seats Taken','Allowed Head Coaches','Allowed Assistant Coaches']
    imp_columns_after_merge = ['PID','Location Acronym','Court Location Abbreviation','Latitude','Longitude','Dates','Days','Start Time', 'End Time','Age Group','Level','Seats Taken','Allowed Head Coaches','Allowed Assistant Coaches','Coach']
    final_df = merged_df[imp_columns_after_merge]

    # Calculate Start and End times, Job durations for programs and make their columns
    final_df['Start Time'] = pd.to_datetime(final_df['Start Time'])
    final_df['End Time'] = pd.to_datetime(final_df['End Time'])
    final_df['Job Time'] = ((final_df['End Time']-final_df['Start Time']).dt.total_seconds() / 60).astype(int)
    final_df['Start Time'] = pd.to_datetime(final_df['Start Time']).dt.time
    final_df['End Time'] = pd.to_datetime(final_df['End Time']).dt.time
    

    # Calculate Number of head and assistant coaches required and make their columns
    final_df['Seats Taken']=final_df['Seats Taken'].astype(int)
    final_df['Required Head Coaches']=None
    final_df['Required Assistant Coaches']=None
    for i in range(len(final_df)):
        if final_df.loc[i,'Level']=='Tod':
            if int(final_df.loc[i,'Seats Taken'])<=3:
                final_df.loc[i,'Required Head Coaches']=1
                final_df.loc[i,'Required Assistant Coaches']=0
            elif int(final_df.loc[i,'Seats Taken'])>3 and int(final_df.loc[i,'Seats Taken'])<=8:
                final_df.loc[i,'Required Head Coaches']=1
                final_df.loc[i,'Required Assistant Coaches']=1
            elif int(final_df.loc[i,'Seats Taken'])>8:
                final_df.loc[i,'Required Head Coaches']=2
                final_df.loc[i,'Required Assistant Coaches']=0
        elif final_df.loc[i,'Level']=='Beg':
            if final_df.loc[i,'Age Group']=='5 - 7':
                if int(final_df.loc[i,'Seats Taken'])<=10:
                    final_df.loc[i,'Required Head Coaches']=1
                    final_df.loc[i,'Required Assistant Coaches']=0
                elif int(final_df.loc[i,'Seats Taken'])>10 and int(final_df.loc[i,'Seats Taken'])<=20:
                    final_df.loc[i,'Required Head Coaches']=1
                    final_df.loc[i,'Required Assistant Coaches']=1
                elif int(final_df.loc[i,'Seats Taken'])>20:
                    final_df.loc[i,'Required Head Coaches']=2
                    final_df.loc[i,'Required Assistant Coaches']=0
            else:
                if int(final_df.loc[i,'Seats Taken'])<=15:
                    final_df.loc[i,'Required Head Coaches']=1
                    final_df.loc[i,'Required Assistant Coaches']=0
                elif int(final_df.loc[i,'Seats Taken'])>15 and int(final_df.loc[i,'Seats Taken'])<=30:
                    final_df.loc[i,'Required Head Coaches']=1
                    final_df.loc[i,'Required Assistant Coaches']=1
                elif int(final_df.loc[i,'Seats Taken'])>30:
                    final_df.loc[i,'Required Head Coaches']=2
                    final_df.loc[i,'Required Assistant Coaches']=0
        else:
            if int(final_df.loc[i,'Seats Taken'])<=15:
                final_df.loc[i,'Required Head Coaches']=1
                final_df.loc[i,'Required Assistant Coaches']=0
            else:
                final_df.loc[i,'Required Head Coaches']=1
                final_df.loc[i,'Required Assistant Coaches']=1

    # Create preferred/ filtered coaches columns on final_df 
    final_df['Filtered Coaches'] = None
    for i in range(len(final_df)):
        filtered_coaches = []
        if final_df.loc[i,'Age Group'] in [ '2 - 5', '2 - 3', '3 - 5']:
            for j in final_df.loc[i,'Allowed Head Coaches'].split(','):
                if df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Age Group'] in [ '2 - 5', '2 - 3', '3 - 5']:
                    filtered_coaches.append(j)
                df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Days Off']
            final_df.loc[i,'Filtered Coaches']=','.join(filtered_coaches)   
        else:
            final_df.loc[i,'Filtered Coaches'] = final_df.loc[i,'Allowed Head Coaches']
        filtered_coaches=final_df.loc[i,'Filtered Coaches'].split(',')
        if filtered_coaches==['']:
            filtered_coaches=[]
        new_filtered_coaches = []
        for j in filtered_coaches:
            if pd.isnull(df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Days Off']):
                new_filtered_coaches.append(j)
            elif df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Days Off'] in final_df.loc[i,'Days']:
                continue
            else:
                new_filtered_coaches.append(j)
        if new_filtered_coaches==[''] or new_filtered_coaches==[]:
            final_df.loc[i,'Filtered Coaches']=None
        else:
            final_df.loc[i,'Filtered Coaches']=','.join(new_filtered_coaches) # Based on Allowed coaches based on Location , then Age Group and if he is present on the date

    final_df['Filtered Assistant Coaches'] = None
    for i in range(len(final_df)):
        filtered_coaches = []
        if final_df.loc[i,'Age Group'] in [ '2 - 5', '2 - 3', '3 - 5']:
            for j in final_df.loc[i,'Allowed Assistant Coaches'].split(','):
                if df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Age Group'] in [ '2 - 5', '2 - 3', '3 - 5']:
                    filtered_coaches.append(j)
                df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Days Off']
            final_df.loc[i,'Filtered Assistant Coaches']=','.join(filtered_coaches)   
        else:
            final_df.loc[i,'Filtered Assistant Coaches'] = final_df.loc[i,'Allowed Assistant Coaches']
        filtered_coaches=final_df.loc[i,'Filtered Assistant Coaches'].split(',')
        if filtered_coaches==['']:
            filtered_coaches=[]
        
        new_filtered_coaches = []
        for j in filtered_coaches:
            if pd.isnull(df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Days Off']):
                new_filtered_coaches.append(j)
            elif df_coaches_profile.loc[df_coaches_profile['Coach ID']==j].iloc[0]['Days Off'] in final_df.loc[i,'Days']:
                continue
            else:
                new_filtered_coaches.append(j)
        if new_filtered_coaches==[''] or new_filtered_coaches==[]:
            final_df.loc[i,'Filtered Assistant Coaches']=None
        else:
            final_df.loc[i,'Filtered Assistant Coaches']=','.join(new_filtered_coaches) # Based on Allowed coaches based on Location , then Age Group and if he is present on the date

    # Drop Allowed coaches and Days columns
    final_df = final_df.drop(columns=['Allowed Head Coaches','Allowed Assistant Coaches','Days'])
    final_df.rename(columns={'Filtered Coaches': 'Filtered Head Coaches'}, inplace=True)
    return final_df


























def get_latest_coach(row,df_history,name_to_coachid):
    if pd.isnull(row['assigned_coaches']):
        program_rows = df_history[df_history['program_id'] == row['program_id']]
        if program_rows.empty:
            return None
        else:
            latest_row = program_rows.sort_values('dates', ascending=False).iloc[0]
            if pd.isnull(latest_row['assigned_coaches']):
                return None
            else:
                coach_id = latest_row['assigned_coaches']
                return coach_id
    else:
        return row['assigned_coaches']

def get_travel_segments(events):
    return zip(events[:-1], events[1:])
def get_home_location(coach,df_coaches_profile):
    last_location_lat = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lat'].iloc[0]
    last_location_lon = df_coaches_profile.loc[df_coaches_profile['coach_id'] == coach, 'home_lang'].iloc[0]
    return (last_location_lat, last_location_lon)
def get_travel_time_to_first_event(coach,coaches_curr_day_busy_schedule_dict,df_coaches_profile):
    if coach in ['TBH','TBC']:
        # print('oye')
        return None
    home_location = get_home_location(coach,df_coaches_profile)
    events = coaches_curr_day_busy_schedule_dict.get(coach, [])
    if events:
        first_event_location = events[0].latitude, events[0].longitude
        return calculate_travel_time_in_minutes(home_location, first_event_location)
    else:
        return None

def get_event_time_location(group):
    event = list(zip(group['start_time'], group['end_time'],group['latitude'],group['longitude'],group['school'],group['court']))
    return event

def process_programs_schedule2(df_programs_schedule):
    df_programs_schedule = df_programs_schedule.copy(deep=True)
    df_programs_schedule['start_date'] = pd.to_datetime(df_programs_schedule['start_date'],format='%Y-%m-%d')
    df_programs_schedule['end_date'] = pd.to_datetime(df_programs_schedule['end_date'],format='%Y-%m-%d')
    df_programs_schedule['dates_no_session'] = df_programs_schedule['dates_no_session'].apply(lambda x: pd.to_datetime([date for date in x], format='%Y-%m-%d') if x else [])
    ### If ABOVE DOESNT WORK THEN PREPROCESSING REQUIRED IN PROGRAMS_SCHEDULE FILE
    # df_programs_schedule['Start Date'] = pd.to_datetime(df_programs_schedule['Start Date'])
    # df_programs_schedule['End Date'] = df_programs_schedule['Start Date'] + pd.to_timedelta(df_programs_schedule['Weeks']*7, unit='d')
    # df_programs_schedule['Start Date'] = df_programs_schedule['Start Date'].dt.strftime('%d-%m-%Y').astype(str) # Use this at the time of saving the csv for Readability
    # df_programs_schedule['End Date'] = df_programs_schedule['End Date'].dt.strftime('%d-%m-%Y').astype(str) # Use this at the time of saving the csv for Readability
    # df_programs_schedule.to_csv(programs_schedule_file_path, index=False)
    df_programs_schedule['dates'] = df_programs_schedule.apply(lambda row: pd.date_range(start=row['start_date'], end=row['end_date']).difference(row['dates_no_session']), axis=1)
    df_programs_schedule = df_programs_schedule.explode('dates')
    df_programs = df_programs_schedule[df_programs_schedule.apply(lambda row: row['dates'].strftime('%a') in [day for day in row['day'].split(',')], axis=1)]
    df_programs = df_programs.reset_index(drop=True)
    return df_programs


def process_data2(df_programs_schedule, df_locations_profile, df_coaches_profile):
    # Your code here
    df_programs = process_programs_schedule2(df_programs_schedule)
    merged_df = df_programs.merge(df_locations_profile, left_on='school', right_on='acronym', how='left')
    all_columns_after_merge = ['program_id', 'school', 'court', 'suggested_coaches',
       'assigned_coaches', 'day', 'start_time', 'end_time', 'name_x', 'level',
       'class_type', 'age_group', 'seat_capacity', 'seats_taken', 'free_seats',
       'start_date', 'end_date', 'weeks', 'dates_no_session', 'term', 'dates',
       'acronym', 'name_y', 'latitude', 'longitude', 'documented_coach',
       'head_coaches', 'assistant_coaches', 'location', 'location_map',
       'courts', 'provider', 'storage', 'stored', 'special_location']
    imp_columns_after_merge = ['program_id','school','court','latitude','longitude','dates','day','start_time', 'end_time','age_group','level','seats_taken','head_coaches','assistant_coaches','assigned_coaches']
    final_df = merged_df[imp_columns_after_merge]

    # Calculate Start and End times, Job durations for programs and make their columns
    final_df['start_time'] = pd.to_datetime(final_df['start_time'])
    final_df['end_time'] = pd.to_datetime(final_df['end_time'])
    final_df['job_time'] = ((final_df['end_time']-final_df['start_time']).dt.total_seconds() / 60).astype(int)
    final_df['start_time'] = pd.to_datetime(final_df['start_time']).dt.time
    final_df['end_time'] = pd.to_datetime(final_df['end_time']).dt.time  

    # Calculate Number of head and assistant coaches required and make their columns
    final_df['seats_taken']=final_df['seats_taken'].astype(int)
    final_df['required_head_coaches']=None
    final_df['required_assistant_coaches']=None
    for i in range(len(final_df)):
        if int(final_df.loc[i,'level'])==1:
            if int(final_df.loc[i,'seats_taken'])<=3:
                final_df.loc[i,'required_head_coaches']=1
                final_df.loc[i,'required_assistant_coaches']=0
            elif int(final_df.loc[i,'seats_taken'])>3 and int(final_df.loc[i,'seats_taken'])<=8:
                final_df.loc[i,'required_head_coaches']=1
                final_df.loc[i,'required_assistant_coaches']=1
            elif int(final_df.loc[i,'seats_taken'])>8:
                final_df.loc[i,'required_head_coaches']=2
                final_df.loc[i,'required_assistant_coaches']=0
        elif int(final_df.loc[i,'level'])==2:
            if int(final_df.loc[i,'age_group'])==2:
                if int(final_df.loc[i,'seats_taken'])<=10:
                    final_df.loc[i,'required_head_coaches']=1
                    final_df.loc[i,'required_assistant_coaches']=0
                elif int(final_df.loc[i,'seats_taken'])>10 and int(final_df.loc[i,'seats_taken'])<=20:
                    final_df.loc[i,'required_head_coaches']=1
                    final_df.loc[i,'required_assistant_coaches']=1
                elif int(final_df.loc[i,'seats_taken'])>20:
                    final_df.loc[i,'required_head_coaches']=2
                    final_df.loc[i,'required_assistant_coaches']=0
            else:
                if int(final_df.loc[i,'seats_taken'])<=15:
                    final_df.loc[i,'required_head_coaches']=1
                    final_df.loc[i,'required_assistant_coaches']=0
                elif int(final_df.loc[i,'seats_taken'])>15 and int(final_df.loc[i,'seats_taken'])<=30:
                    final_df.loc[i,'required_head_coaches']=1
                    final_df.loc[i,'required_assistant_coaches']=1
                elif int(final_df.loc[i,'seats_taken'])>30:
                    final_df.loc[i,'required_head_coaches']=2
                    final_df.loc[i,'required_assistant_coaches']=0
        else:
            if int(final_df.loc[i,'seats_taken'])<=15:
                final_df.loc[i,'required_head_coaches']=1
                final_df.loc[i,'required_assistant_coaches']=0
            else:
                final_df.loc[i,'required_head_coaches']=1
                final_df.loc[i,'required_assistant_coaches']=1

    # Create preferred/ filtered coaches columns on final_df 
    final_df['filtered_coaches'] = None
    for i in range(len(final_df)):
        filtered_coaches = []
        if int(final_df.loc[i,'age_group']) == 1:
            for j in final_df.loc[i,'head_coaches']:
                if (not pd.isnull(df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['age_group'])) and (int(df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['age_group']) ==1):
                    filtered_coaches.append(j)
                df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['days_off']
            final_df.at[i,'filtered_coaches']=filtered_coaches 
        else:

            final_df.at[i,'filtered_coaches'] = final_df.loc[i,'head_coaches']
            
        filtered_coaches=final_df.loc[i,'filtered_coaches']
        if filtered_coaches==['']:
            filtered_coaches=[]
        new_filtered_coaches = []
        for j in filtered_coaches:
            if pd.isnull(df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['days_off']):
                new_filtered_coaches.append(j)
            elif final_df.loc[i,'day'] in df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['days_off']:
                continue
            else:
                new_filtered_coaches.append(j)
        if new_filtered_coaches==[''] or new_filtered_coaches==[]:
            final_df.at[i,'filtered_coaches']=None
        else:
            final_df.at[i,'filtered_coaches']=new_filtered_coaches # Based on Allowed coaches based on Location , then Age Group and if he is present on the date

    final_df['filtered_assistant_coaches'] = None
    for i in range(len(final_df)):
        filtered_coaches = []
        if final_df.loc[i,'age_group'] == 1:
            for j in final_df.loc[i,'assistant_coaches']:
                if (not pd.isnull(df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['age_group'])) and (int(df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['age_group']) ==1):
                    filtered_coaches.append(j)
            final_df.at[i,'filtered_assistant_coaches']=filtered_coaches
        else:
            final_df.at[i,'filtered_assistant_coaches'] = final_df.loc[i,'assistant_coaches']
        filtered_coaches=final_df.loc[i,'filtered_assistant_coaches']
        if filtered_coaches==['']:
            filtered_coaches=[]
        
        new_filtered_coaches = []
        for j in filtered_coaches:
            if pd.isnull(df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['days_off']):
                new_filtered_coaches.append(j)
            elif final_df.loc[i,'day'] in df_coaches_profile.loc[df_coaches_profile['coach_id']==j].iloc[0]['days_off']:
                continue
            else:
                new_filtered_coaches.append(j)
        if new_filtered_coaches==[''] or new_filtered_coaches==[]:
            final_df.at[i,'filtered_assistant_coaches']=None
        else:
            final_df.at[i,'filtered_assistant_coaches']=new_filtered_coaches # Based on Allowed coaches based on Location , then Age Group and if he is present on the date

    # Drop Allowed coaches and Days columns
    final_df = final_df.drop(columns=['head_coaches','assistant_coaches','day'])
    final_df.rename(columns={'filtered_coaches': 'filtered_head_coaches'}, inplace=True)
    return final_df