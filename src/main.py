from weather_api import *
from datetime import datetime, timedelta
import time
import numpy as np
from sense_hat import SenseHat
import json
import os


sense = SenseHat()
sense.low_light = True


def get_time_frames():
        time = datetime.now() + timedelta(hours=1)
        forecast_start = time.strftime("%Y-%m-%dT%H:00:00Z")
        time = time + timedelta(hours=23)
        forecast_end = time.strftime("%Y-%m-%dT%H:00:00Z")

        time = datetime.now()
        observation_end = time.strftime("%Y-%m-%dT%H:00:00Z")
        time = time = time - timedelta(hours=24)
        observation_start = time.strftime("%Y-%m-%dT%H:00:00Z")

        return observation_start, observation_end, forecast_start, forecast_end


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


def write_to_file(o_times, f_times, s_times, o_values, f_values, s_values):
    f_zip = zip(f_times, f_values)
    s_zip = zip(s_times, s_values.tolist())
    o_zip = zip(o_times, o_values)

    f_json_string = json.dumps(dict(f_zip))
    s_json_string = json.dumps(dict(s_zip))
    o_json_string = json.dumps(dict(o_zip))

    with open(os.path.join(os.getcwd(), 'forecastData.json'), 'w') as file:
        file.write(f_json_string)

    with open(os.path.join(os.getcwd(), 'sensorData.json'), 'w') as file:
        file.write(s_json_string)

    with open(os.path.join(os.getcwd(), 'observationData.json'), 'w') as file:
        file.write(o_json_string)


def main():
    i = 0

    # Sensor values
    s_values = np.full(24, 15)
    s_times = ["NaN"] * 24

    while True:
        sense.clear()
        yellow_warning = False
        red_warning = False

        # Timeframes for last 24H observations and next 24H forecast
        o_start, o_end, f_start, f_end = get_time_frames()

         # Temperature forecast, observation and current reading
        f_times, f_values = get_temperature_forecast("Tampere", f_start, f_end)
        o_times, o_values = get_temperature_observations("Tampere", o_start, o_end)
        s_values[i] = sense.get_temperature()
        s_times[i] = datetime.now().strftime("%Y-%m-%dT%H:00:00Z")
        
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
       
        write_to_file(o_times, f_times, s_times,  o_values, f_values, s_values)

        time.sleep(3600)
        i += 1
        i = i % 24


if __name__ == "__main__":
    main()


