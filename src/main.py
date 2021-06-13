from weather_api import *
from datetime import datetime, timedelta
import time
import numpy as np
from sense_hat import SenseHat


sense = SenseHat()
sense.low_light = True


def getTimeFrame():
        time = datetime.now() + timedelta(hours=1)
        start = time.strftime("%Y-%m-%dT%H:00:00Z")
        time = time + timedelta(hours=23)
        end = time.strftime("%Y-%m-%dT%H:00:00Z")

        return start, end


def readTemperature():
    return sense.get_temperature()


def showWarning(colour):
    end_time = datetime.now() + timedelta(hours=1)

    while end_time > datetime.now():
        sense.show_message("!!!", text_colour = colour)


def main():
    i = 0
    values = np.zeros(24)

    while True:
        yellow_warning = False
        red_warning = False
        start, end = getTimeFrame()

        # Temeprature forecast and current reading
        times, forecast_values = apiRequest("Tampere", start, end)
        values[i] = readTemperature()
        
        for temperature in forecast_values:
            if float(temperature) < 10:
                yellow_warning = True
        
        for temperature in values:
            if temperature < 15:
                red_warning = True
                
        if yellow_warning and not red_warning:
            showWarning([255, 255, 0])
        elif red_warning:
            showWarning([255, 0, 0])
        else:
            time.sleep(3600)

        i += 1
        i = i % 24


if __name__ == "__main__":
    main()