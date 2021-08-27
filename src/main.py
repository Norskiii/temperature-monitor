from weather_api import *
from db_connection import *
from datetime import datetime, timedelta
import time
import numpy as np
from sense_hat import SenseHat
import os


sense = SenseHat()
sense.low_light = True


def get_time_frames():
    now = datetime.now() + timedelta(hours=1)
    forecast_start = now.strftime("%Y-%m-%dT%H:00:00Z")
    now = now + timedelta(hours=23)
    forecast_end = now.strftime("%Y-%m-%dT%H:00:00Z")

    now = datetime.now()
    observation_end = now.strftime("%Y-%m-%dT%H:00:00Z")
    now = now - timedelta(hours=24)
    observation_start = now.strftime("%Y-%m-%dT%H:00:00Z")

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


def formatDatetimeToHours(times):
    hours = []

    for dt in times:
        hours.append(datetime.strptime(dt, "%Y-%m-%dT%H:00:00Z").strftime("%H"))

    return hours


def main():
    i = 0

    # Sensor values
    s_values = ["15"] * 24
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
        f_times = formatDatetimeToHours(f_times)
        o_times = formatDatetimeToHours(o_times)
        s_values[i] = str(np.round(sense.get_temperature(), 1))
        s_times[i] = datetime.now().strftime("%H")

        for temperature in f_values:
            if float(temperature) < 10:
                yellow_warning = True
        
        for temperature in s_values:
            if float(temperature) < 15:
                red_warning = True
                
        if yellow_warning and not red_warning:
            show_warning([255, 255, 0])
        elif red_warning:
            show_warning([255, 0, 0])
        else:
            all_ok()
        
        write_to_db(o_times, f_times, s_times,  o_values, f_values, s_values)

        time.sleep(3600)
        i += 1
        i = i % 24


if __name__ == "__main__":
    main()


