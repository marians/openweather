# encoding: utf-8

import openweather
import unittest
from datetime import datetime
from datetime import timedelta


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.ow = openweather.OpenWeather()
        self.station_ids = [4885]  # Airport Cologne/Bonn

    def test_find_stations_1(self):
        stations = self.ow.find_stations_near(7.0, 50.0, 100)
        self.assertIs(type(stations), dict)
        self.assertTrue("list" in stations)
        self.assertIs(type(stations["list"]), list)

    def test_get_weather_1(self):
        weather = self.ow.get_weather(self.station_ids[0])
        self.assertIs(type(weather), dict)
        self.assertTrue("id" in weather)
        self.assertTrue("main" in weather)
        self.assertTrue("name" in weather)
        self.assertTrue("coord" in weather)
        self.assertTrue("station" in weather)
        self.assertTrue("calc" in weather)
        self.assertTrue("wind" in weather)

    def test_get_historic_weather_1(self):
        start = datetime.utcnow() - timedelta(days=5)
        end = start + timedelta(days=1)
        weather = self.ow.get_historic_weather(
            station_id=self.station_ids[0],
            from_date=start,
            to_date=end)
        self.assertIs(type(weather), list)
        self.assertTrue("calc" in weather[0])
        self.assertTrue("temp" in weather[0])
        self.assertTrue("humidity" in weather[0])
        self.assertTrue("pressure" in weather[0])
        self.assertTrue("main" in weather[0])
        self.assertTrue("dt" in weather[0])
        self.assertTrue("wind" in weather[0])

if __name__ == '__main__':
    unittest.main()
