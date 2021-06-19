import requests
import xml.etree.ElementTree as ET

def getTemperatureForecast(location, start, end):
    url = "https://opendata.fmi.fi/wfs?request=getFeature&version=2.0.0&storedquery_id=fmi::forecast::hirlam::surface::point::simple&&place=" + \
          location + "&timestep=60&starttime=" + \
          start + "&endtime=" + \
          end + "&parameters=temperature"

    r = requests.get(url)
    
    return parseXML(r.text)


def getTemperatureObservations(location, start, end):
    url = "https://opendata.fmi.fi/wfs?request=getFeature&version=2.0.0&storedquery_id=fmi::observations::weather::hourly::simple&&place=" + \
          location + "&timestep=60&starttime=" + \
          start + "&endtime=" + \
          end + "&parameters=TA_PT1H_AVG"

    r = requests.get(url)
    
    return parseXML(r.text)


def parseXML(content):
    times = []
    values = []
    root = ET.fromstring(content)

    for i in range(0,24):
        times.insert(i, root[i][0][1].text)
        values.insert(i, root[i][0][3].text)

    return times, values