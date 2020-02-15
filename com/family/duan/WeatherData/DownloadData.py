from typing import TextIO, Dict, List
from datetime import date, timedelta
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import requests
import csv

start_date = date(2013, 1, 1)  # start date
end_date = date(2013, 4, 27)  # end date
delta = end_date - start_date  # timedelta

target_dates: List[date] = []
for i in range(delta.days + 1):
    target_dates.append(start_date + timedelta(i))

# WebApi token
#headers = {'token': ''} #duanxingjian
headers = {'token': ''} # paradiseleaf

region_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations"

region_payload: Dict[str, str] = dict(
    datasetid="GHCND",
    datacategoryid="TEMP",
    startdate="2009-4-28",
    enddate="2019-4-28",
    limit="50",
    locationcategoryid="CLIM_REG",
)

# GHCN (Global Historical Climatology Network)-Daily
# https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn
data_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

data_payload: Dict[str, str] = dict(datasetid="GHCND",
                                    datatypeid="TAVG",
                                    limit="1000",
                                    units="metric")

region_response = requests.get(region_url, headers=headers, params=region_payload)
region_response = region_response.json()
regions = region_response['results']

weather_data_file: TextIO = open('WeatherData.csv', "w",
                                 newline='\n', encoding="utf-8")
csv_writer = csv.writer(weather_data_file)

# Write CSV Header
csv_writer.writerow(["date", "datatype", "station", "avg_temp", "region"])

for target_date in target_dates:
    target_date_str: str = target_date.strftime('%Y-%m-%d')
    for region in regions:
        print(target_date_str + " " + region['name'])

        region_name = region['name']
        region_id = region['id']
        # Loop through all locs
        data_payload.update({"locationid": region_id})

        # Loop through all dates
        data_payload.update({"startdate": target_date_str})
        data_payload.update({"enddate": target_date_str})

        req_session = requests.Session()

        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        req_session.mount('http://', HTTPAdapter(max_retries=retries))

        data_response: Response = req_session.get(data_url, headers=headers, params=data_payload)
        data_response = data_response.json()

        # Write CSV body
        for row in data_response['results']:
            csv_writer.writerow([row["date"],
                                 row["datatype"],
                                 row["station"],
                                 row["value"],
                                 region_name])

weather_data_file.close()
