import os
import psycopg2
import json
import subprocess
from datetime import datetime
import time

def check_for_nan_values(values):
    new_values = []

    for i in range(len(values)):
        if values[i] == "NaN":
            new_values.append(-100)
        else:
            new_values.append(float(values[i]))

    return new_values


def write_to_db(o_times, f_times, s_times, o_values, f_values, s_values):
    # Check all lists for NaN values
    o_values = check_for_nan_values(o_values)
    f_values = check_for_nan_values(f_values)
    s_values = check_for_nan_values(s_values)
    
    # Lists for observation, forecast and sensor datareadings
    # For each reading an id, time(current hour) and value will be saved
    o_data = []
    f_data = []
    s_data = []

    # Save datapoints into lists in correct dataformats
    for i in range(len(o_values)):
        o_data.append({'x':o_times[i], 'y':o_values[i]}) 
    
    for i in range(len(f_values)):
        f_data.append({'x':f_times[i], 'y':f_values[i]})

    for i in range(len(s_values)):
        s_data.append({'x':s_times[i], 'y':s_values[i]})
 
    # Cornvert lists into JSON strings what will be saved to the database
    o_json = json.dumps(o_data)
    f_json = json.dumps(f_data)
    s_json = json.dumps(s_data)

    records = [(o_json, 1),
               (f_json, 2),
               (s_json, 3)]
    
    result = subprocess.run(['heroku','config:get','DATABASE_URL', '-a', 'norski-live'], stdout=subprocess.PIPE)
    url = result.stdout.decode('ascii').strip()
    #print("Connecting to database url:", url, flush=True)
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    try:
        connection = psycopg2.connect(url, sslmode='require')
        cursor = connection.cursor()

        query = """UPDATE data SET data = %s WHERE id = %s"""
        cursor.executemany(query, records)
        connection.commit()

        count = cursor.rowcount
        print(timestamp, count, "Rows updated", end='\r', flush=True)

    except (Exception, psycopg2.Error) as error:
        print(timestamp, "Error while updating table", error, flush=True)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print(timestamp, "PostgreSQL connection is closed", end='\r', flush=True)

