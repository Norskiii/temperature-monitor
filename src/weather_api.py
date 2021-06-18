import requests
import xml.etree.ElementTree as ET

def apiRequestNext24H(location, start, end):
    url = "https://opendata.fmi.fi/wfs?request=getFeature&version=2.0.0&storedquery_id=fmi::forecast::hirlam::surface::point::simple&&place=" + \
          location + "&timestep=60&starttime=" + \
          start + "&endtime=" + \
          end + "&parameters=temperature"

    r = requests.get(url)
    
    return parseXML(r.text)


def apiRequestLast24H(location, start, end):
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


def main():
    times1, values1 = apiRequestLast24H("Tampere", "2021-06-17T20:00:00Z", "2021-06-18T19:00:00Z")
    times2, values2 = apiRequestNext24H("Tampere", "2021-06-18T20:00:00Z", "2021-06-19T19:00:00Z")

    print("Last 24H:")  
    for i in range(0, 24):
        print("Time:", times1[i])
        print("Temp: ", values1[i])


    print("Next 24H:")  
    for i in range(0, 24):
        print("Time:", times2[i])
        print("Temp: ", values2[i])


if __name__ == "__main__":
    main()