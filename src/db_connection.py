import os
import psycopg2
import json
import subprocess


def write_to_db(o_times, f_times, s_times, o_values, f_values, s_values):
    # Lists for observation, forecast and sensor datareadings
    # For each reading an id, time(current hour) and value will be saved
    o_data = []
    f_data = []
    s_data = []

    # Save datapoints into lists in correct dataformats
    for i in range(len(o_values)):
        o_data.append({'id':i, 'time':o_times[i], 'value':o_values[i]}) 
    
    for i in range(len(f_values)):
        f_data.append({'id':i, 'time':f_times[i], 'value':f_values[i]})

    for i in range(len(s_values)):
        s_data.append({'id':i, 'time':s_times[i], 'value':s_values[i]})
 
    # Cornvert lists into JSON strings what will be saved to the database
    o_json = json.dumps(o_data)
    f_json = json.dumps(f_data)
    s_json = json.dumps(s_data)

    records = [(o_json, 1),
               (f_json, 2),
               (s_json, 3)]
    
    result = subprocess.run(['heroku','config:get','DATABASE_URL', '-a', 'norski-live'], stdout=subprocess.PIPE)
    url = result.stdout.decode('ascii').strip()
    print(url, flush=True)

    try:
        connection = psycopg2.connect(url, sslmode='require')
        cursor = connection.cursor()

        query = """UPDATE data SET data = %s WHERE id = %s"""
        cursor.executemany(query, records)
        connection.commit()

        count = cursor.rowcount
        print(count, "Rows updated", flush=True)

    except (Exception, psycopg2.Error) as error:
        print("Error while updating table", error, flush=True)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed", flush=True)

