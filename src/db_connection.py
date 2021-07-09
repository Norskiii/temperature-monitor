import os
import psycopg2
import json


def write_to_db(o_times, f_times, s_times, o_values, f_values, s_values):
    o_zip = zip(o_times, o_values)
    f_zip = zip(f_times, f_values)
    s_zip = zip(s_times, s_values)

    o_json_string = json.dumps(dict(o_zip))
    f_json_string = json.dumps(dict(f_zip))
    s_json_string = json.dumps(dict(s_zip))

    records = [(o_json_string, 1),
               (f_json_string, 2),
               (s_json_string, 3)]

    url = os.environ.get('DATABASE_URL')

    try:
        connection = psycopg2.connect(url, sslmode='require')
        cursor = connection.cursor()

        query = """UPDATE data SET json = %s WHERE id = %s"""
        cursor.executemany(query, records)
        connection.commit()

        count = cursor.rowcount
        print(count, "Rows updated")

    except (Exception, psycopg2.Error) as error:
        print("Error while updating table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


