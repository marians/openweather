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
python -m openweather -s 4885
```

Print historic weather at station ID 4885:

```sh
python -m openweather -s 4885 --historic
```

Print historic weather for 2013-10-01 at station ID 4885:

```sh
python -m openweather -s 4885 --historic --date 20131001
```

For valid formats of the `--date` parameter, see [daterangestr](https://github.com/marians/py-daterangestr).

Print historic data in CSV format

python openweather.py -s 4885 --historic --date 20131022 --csv|csvcut -c 10,14,23,25|csvlook

This is particularly usefull if you want to store that data to a file...

```sh
python -m openweather -s 4885 --historic --date 20131022 --csv > weather.csv
```

... or want to manipulate and display it (using [csvkit](https://github.com/onyxfish/csvkit)):

```sh
python openweather.py -s 4885 --historic --date 20131022 --csv|csvcut -c 10,14,23,25|csvlook
|-------------+-----------+----------+-------------|
|  dt         | main_temp | wind_deg | wind_speed  |
|-------------+-----------+----------+-------------|
|             |           |          |             |
|  1382817000 | 291.15    | 160      | 3.6         |
|  1382818800 | 291.15    | 160      | 4.1         |
|  1382822400 | 291.15    | 140      | 3.6         |
|  1382822400 | 291.15    | 140      | 3.6         |
|  1382826000 | 290.15    | 170      | 4.1         |
...
|  1382872800 | 290.15    | 220      | 9.8         |
|  1382874600 | 289.15    | 210      | 9.3         |
|-------------+-----------+----------+-------------|
```
