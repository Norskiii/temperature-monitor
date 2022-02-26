from fmiopendata.wfs import download_stored_query
import datetime as dt
import math


def get_temperature_forecast():
    start_time = dt.datetime.utcnow() + dt.timedelta(hours=2)
    end_time = start_time + dt.timedelta(hours=24)

    start_time = start_time.isoformat(timespec='seconds') + 'Z'
    end_time = end_time.isoformat(timespec='seconds') + 'Z'
    try:
        obs = download_stored_query('fmi::forecast::hirlam::surface::obsstations::multipointcoverage', \
                args=['timeseries=True', \
                'starttime=' + start_time, \
                'endtime=' + end_time])
    
        location = 'Tampere-Pirkkala airport'

        times = [time.strftime("%d.%m. %H:00") for time in obs.data[location]['times']]
        values = obs.data[location]['Temperature']['values'] 

        for i in range(len(values)):
            if math.isnan(values[i]):
                values[i] = values[i-1]
    except:
        print('Failed to retrieve weather data')
        times = []
        values = []
        
    return times, values


def get_temperature_observations():
    end_time = dt.datetime.utcnow() + dt.timedelta(hours=2)
    start_time = end_time - dt.timedelta(hours=24)

    start_time = start_time.isoformat(timespec='seconds') + 'Z'
    end_time = end_time.isoformat(timespec='seconds') + 'Z'
    try:
        obs = download_stored_query('fmi::observations::weather::multipointcoverage', \
                                    args=['bbox=23.63,61.44,23.78,61.5',\
                                        'timeseries=True', \
                                        'timestep=60', \
                                        'starttime=' + start_time, \
                                        'endtime=' + end_time])

        location = sorted(obs.data.keys())[0]

        times = [time.strftime("%d.%m. %H:00") for time in obs.data[location]['times']]
        values = obs.data[location]['t2m']['values'] 

        for i in range(len(values)):
            if math.isnan(values[i]):
                values[i] = values[i-1]
    except:
        print('Could not retrieve weather data')
        times = []
        values = []

    return times, values
