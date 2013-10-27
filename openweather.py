# encoding: utf-8

"""
API docs available at
http://openweathermap.org/wiki/API/2.1/JSON_API
"""

import json
import urllib
from datetime import datetime


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

    def get_weather(self, station_id):
        """
        Returns recent weather data for given station
        """
        url = (self.base_url +
            '/weather/station/%d?type=json'
            % station_id)
        data = self.do_request(url)
        return data

    def get_historic_weather(self, station_id,
            from_date=None, to_date=None,
            resolution='hour'):
        """
        Loads historic values from given station. Start and end date have
        to be given as datetime objects.
        """
        if resolution not in ['tick', 'hour', 'day']:
            raise ValueError('Resolution has to be "tick", "hour" or "day".')
        from_ts = ''
        to_ts = ''
        if type(from_date) == datetime:
            from_ts = from_date.strftime('%s')
        if type(to_date) == datetime:
            to_ts = to_date.strftime('%s')
        url = (self.base_url +
            '/history/station/%d?type=%s&start=%s&end=%s'
            % (station_id, resolution, from_ts, to_ts))
        data = self.do_request(url)
        if 'list' in data:
            return data['list']

    def do_request(self, url):
        request = urllib.urlopen(url)
        data = request.read()
        data = json.loads(data)
        return data


if __name__ == '__main__':
    """Command line client mode"""
    import argparse
    import daterangestr
    import sys
    parser = argparse.ArgumentParser(description='Get weather information from OpenWeatherMap.')
    parser.add_argument('-s', '--station', dest='station_id', type=int, metavar='STATION',
                   help='Station ID to get information for')
    parser.add_argument('--historic', dest='get_historic', action='store_true',
                   default=False,
                   help='Get historic data instead of recent')
    parser.add_argument('--date', dest='daterange',
                   help='Date range for historic data retrieval, as string YYYYMMDD-YYYYMMDD.')
    args = parser.parse_args()
    if args.station_id is None:
        sys.stderr.write("ERROR: No station ID given. Use -s parameter, e.g. -s 4885.\n")
        sys.exit(1)
    ow = OpenWeather()
    weather = None
    if args.get_historic:
        from_date = None
        to_date = None
        if args.daterange is not None:
            (from_date, to_date) = daterangestr.to_dates(args.daterange)
        weather = ow.get_historic_weather(
            station_id=args.station_id,
            from_date=from_date,
            to_date=to_date,
            resolution="tick")
    else:
        weather = ow.get_weather(args.station_id)
    print json.dumps(weather, indent=4, sort_keys=True)
