# encoding: utf-8

import json
import urllib


class OpenWeather(object):

    def __init__(self):
        self.base_url = 'http://openweathermap.org/data/2.1'

    def find_stations_near(self, lon, lat, radius_limit=20):
        """
        Searches for weather station near a given coordinate and
        returns them, ordered by distance
        """
        url = (self.base_url +
            '/find/station?lat=%s&lon=%s&radius=%d'
            % (lat, lon, radius_limit))
        return self.do_request(url)

    def get_historic_weather(self, station_id, from_date, to_date):
        """
        Loads historic values from given station. Start and end date have
        to be given as datetime objects.
        """
        from_ts = from_date.strftime('%s')
        to_ts = to_date.strftime('%s')
        url = (self.base_url +
            '/history/station/%d?type=hour&start=%s&end=%s'
            % (station_id, from_ts, to_ts))
        return self.do_request(url)

    def do_request(self, url):
        request = urllib.urlopen(url)
        data = request.read()
        data = json.loads(data)
        if 'list' in data:
            return data['list']
