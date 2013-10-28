VERY basic start for a OpenWeatherMap.org API client.

Frankly, it as been written rather to test how Python modules are distributed. :)

##Install

    pip install openweather

##Python module example
    
```python
import openweather
from datetime import datetime

# create client
ow = openweather.OpenWeather()

# find weather stations near me
stations = ow.find_stations_near(
	7.0,  # longitude
	50.0, # latitude
	100   # kilometer radius
)

# iterate results
for station in stations:
	print station

# get current weather at Cologne/Bonn airport
# (station id = 4885)
print ow.get_weather(4885)

# historic weather
start_date = datetime(2013, 09, 10)
end_date = datetime(2013, 09, 15)

# default: hourly interval
print ow.get_historic_weather(4885, start_date, end_date)

# raw data (resolution = "tick")
print ow.get_historic_weather(4885, start_date, end_date, "tick")

# daily aggregates
print ow.get_historic_weather(4885, start_date, end_date, "day")
```

## Command line client example

Print current weather at station ID 4885:

```sh
$ python -m openweather -s 4885
```

Print historic weather at station ID 4885:

```sh
$ python -m openweather -s 4885 --historic
```

Print historic weather for 2013-10-01 at station ID 4885:

```sh
$ python -m openweather -s 4885 --historic --date 20131001
```

For valid formats of the `--date` parameter, see [daterangestr](https://github.com/marians/py-daterangestr).

Print historic data in CSV format

```sh
$ python openweather.py -s 4885 --historic --date 20131022 --csv
```

This is particularly usefull if you want to store that data to a file...

```sh
$ python -m openweather -s 4885 --historic --date 20131022 --csv > weather.csv
```

... or want to manipulate and display it (using [csvkit](https://github.com/onyxfish/csvkit)):

```sh
$ python openweather.py -s 4885 --historic --date 20131027 --csv|csvcut -c 9,26,30,35,43|csvlook
|-------------+-------------+------------+------------+---------------|
|  dt         | main_temp_v | pressure_v | wind_deg_v | wind_speed_v  |
|-------------+-------------+------------+------------+---------------|
|  1382824800 | 287.15      | 1005       |            | 4.1           |
|  1382835600 | 290.4       | 1008.25    | 170        | 5.93          |
|  1382839200 | 289.15      | 1007.5     | 175        | 5.1           |
...
|  1382904000 | 287.15      | 1007       | 210        | 5.9           |
|  1382907600 | 287.15      | 1007       | 200        | 6.2           |
|  1382911200 | 287.15      | 1006       | 177        | 5.1           |
|             |             |            |            |               |
|-------------+-------------+------------+------------+---------------|
```
