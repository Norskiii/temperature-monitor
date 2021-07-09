# temperature-alarm
Temperature alarm with Raspberry Pi Sense HAT. Displays red exclamation mark on the led matrix, if the sensor temperature has dropped below 15 degrees celcius in the last 24 hours. If the outside temperature forecast drops below 10 degrees celsius in the next 24 hours, the led matrix displays a yellow exclamation mark. The forecast values are fetched from [Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data).  

## Requirements
1. Python 3.9
2. Install required packages with `pip install -r requirements.txt`
