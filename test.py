# encoding: utf-8

import openweather
import unittest
from datetime import datetime
from datetime import timedelta
import os


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.ow_nocache = openweather.OpenWeather(cache=False)
        self.ow = openweather.OpenWeather(cache="openweather-unnittest-cache.db")
        self.station_ids = [4885]  # Airport Cologne/Bonn

    def tearDown(self):
        self.ow.cacheconn.close()
        del self.ow
        os.remove("openweather-unnittest-cache.db")

    def test_find_stations_1(self):
        stations = self.ow_nocache.find_stations_near(7.0, 50.0, 100)
        self.assertIs(type(stations), dict)
        self.assertTrue("list" in stations)
        self.assertIs(type(stations["list"]), list)

    def test_get_weather_1(self):
        weather = self.ow_nocache.get_weather(self.station_ids[0])
        self.assertIs(type(weather), dict)
        self.assertTrue("id" in weather)
        self.assertTrue("main" in weather)
        self.assertTrue("name" in weather)
        self.assertTrue("coord" in weather)
        self.assertTrue("station" in weather)
        self.assertTrue("calc" in weather)
        self.assertTrue("wind" in weather)

    def test_get_historic_weather_nocache_1(self):
        start = datetime.utcnow() - timedelta(days=5)
        end = start + timedelta(days=1)
        weather = self.ow_nocache.get_historic_weather(
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

    def test_get_historic_weather_cache_1(self):
        """
        Get data for last day and count number of
        items, check if > 0
        """
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
        self.ow.cache.execute("SELECT COUNT(*) FROM values_hour")
        self.assertTrue(self.ow.cache.fetchone()[0] > 0)

    def test_get_historic_weather_nocache_2(self):
        fromd = datetime(2013, 8, 1, 10)
        tod = datetime(2013, 8, 1, 11)
        weather = self.ow_nocache.get_historic_weather(
            station_id=4885,
            from_date=fromd,
            to_date=tod)
        self.assertIs(type(weather), list)

    def test_get_historic_weather_cache_2(self):
        """
        Request spans 2 hours, but we fetch an entire day to cache.
        """
        fromd = datetime(2013, 8, 1, 10)
        tod = datetime(2013, 8, 1, 11)
        weather = self.ow.get_historic_weather(
            station_id=4885,
            from_date=fromd,
            to_date=tod)
        self.assertIs(type(weather), list)
        self.ow.cache.execute("SELECT COUNT(*) FROM values_hour")
        self.assertTrue(self.ow.cache.fetchone()[0] >= 24)

if __name__ == '__main__':
    unittest.main()
