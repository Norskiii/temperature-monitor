from weather_data import *
from db_connection import *
from datetime import datetime, timedelta
import time
import numpy as np
from sense_hat import SenseHat
import os
from collections import deque
import argparse


sense = SenseHat()
sense.low_light = True


def read_sensor_values():
    times = []
    values = []
    
    with open('sensor.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            x = line.split(',')
            if len(x) == 2:
                times.append(x[0])
                values.append(float(x[1]))

    return times, values


def write_sensor_values(times, values):
    with open('sensor.txt', 'w') as f:
        for i in range(len(values)):
                f.write(str(times[i]) + ", " + str(values[i]))
                f.write('\n')


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


def main():
    parser = argparse.ArgumentParser(description='Temperature monitor using senseHat and Heroku Postgres')
    parser.add_argument('app_name', type=str, help='Name of Heroku app')
    args = parser.parse_args()

    i = 0

    # Sensor values
    s_times, s_values = read_sensor_values()
    s_times = deque(s_times)
    s_values = deque(s_values)
    f_times = []
    f_values = []
    o_times = []
    o_values = []

    # start loop approximately on the hour
    minutes = 60 - (time.time() / 60%60) # minutes until start
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, "Waiting", np.round(minutes,2), "minutes", flush=True)
    time.sleep(round(60*minutes))

    while True:
        sense.clear()
        yellow_warning = False
        red_warning = False

        # Temperature forecast, observation and current reading
        new_f_times, new_f_values = get_temperature_forecast()
        new_o_times, new_o_values = get_temperature_observations()
        
        if new_f_times and new_f_values:
            f_times = new_f_times
            f_values = new_f_values

        if new_o_times and new_o_values:
            o_times = new_o_times
            o_values = new_o_values
            
        s_values.pop()
        s_values.appendleft(str(np.round(sense.get_temperature(), 1)))

        s_times.pop()
        s_times.appendleft(datetime.now().strftime("%d.%m. %H:00"))

        for temperature in f_values:
            if float(temperature) < 10:
                yellow_warning = True
        
        for temperature in s_values:
            if float(temperature) < 15:
                red_warning = True
                
        if yellow_warning and not red_warning:
            #show_warning([255, 255, 0])
            color = (255, 255, 0)
        elif red_warning:
            #show_warning([255, 0, 0])
            color = (255, 0, 0)
        else:
            #all_ok()
            color = (0, 255, 0)
        

        write_to_db(o_times, f_times, list(s_times),  o_values, f_values, list(s_values), args.app_name)
        write_sensor_values(list(s_times), list(s_values))

        #print("Waiting for next update (1H)", flush=True)
        #time.sleep(3600)
        
        iter_time = time.time() + 3600  # time until next iteration start
        while time.time() < iter_time:
            sense.show_message(str(s_values[0])+"C", text_colour=color)
            
        i += 1
        i = i % 24


if __name__ == "__main__":
    main()
