# temperature-monitor
Temperature monitor made with with Raspberry Pi Sense HAT and Heroku Postgres. The code displays current temperature reading with red color on the led matrix, if the temperature has dropped below 15 degrees celcius in the last 24 hours. If the outside temperature forecast drops below 10 degrees celsius in the next 24 hours, the led matrix displays sensor temperature reading with yellow colour. The forecast values are fetched from [Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data). 

## Requirements
1. Python 3.9
2. Heroku app with PostgreSQL add-on
3. Install required packages with `pip install -r requirements.txt`
