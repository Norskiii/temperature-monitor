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
        sense.show_message("!", text_colour = colour, scroll_speed = 0.2)


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
    values = np.full(24, 15)

    while True:
        sense.clear()
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
            allOK()
            time.sleep(3600)

        i += 1
        i = i % 24


if __name__ == "__main__":
    main()
