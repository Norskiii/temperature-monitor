from weather_api import *
from datetime import datetime, timedelta
import time
import numpy as np
from sense_hat import SenseHat
import json
import os


sense = SenseHat()
sense.low_light = True


def get_time_frame():
        time = datetime.now() + timedelta(hours=1)
        start = time.strftime("%Y-%m-%dT%H:00:00Z")
        time = time + timedelta(hours=23)
        end = time.strftime("%Y-%m-%dT%H:00:00Z")

        return start, end


def read_temperature():
    return sense.get_temperature()


def show_warning(colour):
    x = colour
    o = (0, 0, 0)

    warning = [o, o, o, x, x, o, o, o,
            o, o, o, x, x, o, o, o,
            o, o, o, x, x, o, o, o,
            o, o, o, x, x, o, o, o,
            o, o, o, x, x, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, x, x, o, o, o,
            o, o, o, x, x, o, o, o]
    sense.set_pixels(warning)


def all_ok():
    x = (0, 255, 0)
    o = (0, 0, 0)

    ok = [o, o, o, o, o, o, o, o,
            x, x, x, o, x, o, o, x,
            x, o, x, o, x, o, x, o,
            x, o, x, o, x, x, o, o,
            x, o, x, o, x, o, x, o,
            x, x, x, o, x, o, o, x,
            o, o, o, o, o, o, o, o,
            x, x, x, x, x, x, x, x]

    sense.set_pixels(ok)


def write_to_file(times, forecast_values, sensor_values):
    zip_forecast = zip(times, forecast_values)
    zip_sensor = zip(times, sensor_values.tolist())

    forecast_json_string = json.dumps(dict(zip_forecast))
    sensor_json_string = json.dumps(dict(zip_sensor))

    with open(os.path.join(os.getcwd(), '..', '..', 'forecastData.json'), 'w') as file:
        file.write(forecast_json_string)

    with open(os.path.join(os.getcwd(), '..', '..', 'sensorData.json'), 'w') as file:
        file.write(sensor_json_string)


def main():
    i = 0
    # Sensor values
    s_values = np.full(24, 15)

    while True:
        sense.clear()
        yellow_warning = False
        red_warning = False
        start, end = get_time_frame()

        # Temeprature forecast and current reading
        times, f_values = api_request("Tampere", start, end)
        s_values[i] = read_temperature()
        
        for temperature in f_values:
            if float(temperature) < 10:
                yellow_warning = True
        
        for temperature in s_values:
            if temperature < 15:
                red_warning = True
                
        if yellow_warning and not red_warning:
            show_warning([255, 255, 0])
        elif red_warning:
            show_warning([255, 0, 0])
        else:
            all_ok()
       
        write_to_file(times, f_values, s_values)

        time.sleep(3600)
        i += 1
        i = i % 24


if __name__ == "__main__":
    main()
