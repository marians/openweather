VERY basic start for a OpenWeatherMap.org API client.

Frankly, it as been written rather to test how Python modules are distributed. :)

###Install

    pip install openweather

###Example

    import openweather
    ow = openweather.OpenWeather()
    stations = ow.find_stations_near(7.0, 50.0, 100)
    for station in stations:
    	print station
