VERY basic start for a OpenWeatherMap.org API client.

Frankly, it as been written rather to test how Python modules are distributed. :)

###Install

    pip install openweather

###Example

    import openweather

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
