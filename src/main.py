from weather_api import *
from datetime import datetime, timedelta
import time
import numpy as np
from sense_hat import SenseHat


sense = SenseHat()
sense.low_light = True


def getTimeFrames():
        time = datetime.now() + timedelta(hours=1)
        forecast_start = time.strftime("%Y-%m-%dT%H:00:00Z")
        time = time + timedelta(hours=23)
        forecast_end = time.strftime("%Y-%m-%dT%H:00:00Z")

        time = datetime.now() + timedelta(hours=1)
        observation_end = time.strftime("%Y-%m-%dT%H:00:00Z")
        time = time = time - timedelta(hours=23)
        observation_start = time.strftime("%Y-%m-%dT%H:00:00Z")

        return observation_start, observation_end, forecast_start, forecast_end


def readTemperature():
    return sense.get_temperature()


def showWarning(colour):
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


def allOK():
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
    i = 0
    sensor_values = np.full(24, 15)

    while True:
        sense.clear()
        yellow_warning = False
        red_warning = False
        observation_start, observation_end, forecast_start, forecast_end = getTimeFrames()

         # Temperature forecast, observation and current reading
        forecast_times, forecast_values = getTemperatureForecast("Tampere", forecast_start, forecast_end)
        observation_times, observation_values = getTemperatureObservations("Tampere", observation_start, observation_end)
        sensor_values[i] = readTemperature()
        
        for temperature in forecast_values:
            if float(temperature) < 10:
                yellow_warning = True
        
        for temperature in sensor_values:
            if temperature < 15:
                red_warning = True
                
        if yellow_warning and not red_warning:
            showWarning([255, 255, 0])
        elif red_warning:
            showWarning([255, 0, 0])
        else:
            allOK()

        time.sleep(3600)
        i += 1
        i = i % 24


if __name__ == "__main__":
    main()


