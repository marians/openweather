# encoding: utf-8

"""
API docs available at
http://openweathermap.org/current
http://openweathermap.org/api_station
"""

import json
import requests
from requests.adapters import HTTPAdapter
from datetime import datetime
from datetime import timedelta
import collections
import time
import math
import sys
import pickle
import sqlite3


class OpenWeather(object):

    def __init__(self, verbose=False, cache=True):
        """
        verbose: Activate verbose output (default: False)
        cache: Set False to deactivate, set to path string to
            explicitly set cache db path. Default: True
        """
        self.cache_path = "openweather-cache.db"
        self.base_url = 'http://api.openweathermap.org/data/2.5'
        self.verbose = verbose
        self.cache = False
        if cache is not False:
            if cache is not True:
                self.cache_path = cache
            self.cacheconn = sqlite3.connect(self.cache_path)
            self.cache = self.cacheconn.cursor()
            self.cache.execute("""CREATE TABLE IF NOT EXISTS values_hour
                (dt INTEGER, payload BLOB, PRIMARY KEY(dt ASC))""")
            self.cache.execute("""CREATE TABLE IF NOT EXISTS values_day
                (dt INTEGER, payload BLOB, PRIMARY KEY(dt ASC))""")

    def find_stations_near(self, lon, lat, limit=30):
        """
        Searches for weather station near a given coordinate and
        returns them, ordered by distance
        """
        url = (self.base_url +
            '/station/find?lat=%s&lon=%s&cnt=%d'
            % (lat, lon, limit))
        return self.do_request(url)

    def get_weather(self, station_id):
        """
        Returns recent weather data for given station
        """
        url = (self.base_url +
            '/station?id=%d'
            % station_id)
        data = self.do_request(url)
        return data["last"]

    def get_historic_weather(self, station_id,
            from_date=None, to_date=None,
            resolution='hour'):
        """
        Loads historic values from given station. Start and end date have
        to be given as datetime objects. Data is only requested from the
        server if it's not contained in the database. API results are
        cached in the database.
        """
        if resolution not in ['hour', 'day']:
            raise ValueError('Resolution has to be "hour" or "day".')
        from_ts = ''
        to_ts = ''
        if isinstance(from_date, datetime):
            from_ts = int(from_date.strftime('%s'))
        if isinstance(to_date, datetime):
            to_ts = int(to_date.strftime('%s'))
        # counting record in DB
        if self.cache:
            self.cache.execute("SELECT COUNT(*) FROM values_%s WHERE dt >= ? AND dt <= ?" % resolution,
                [from_ts, to_ts])
            result = self.cache.fetchone()
            rows_expected = (to_ts - from_ts) / 60 / 60
            if resolution == 'day':
                rows_expected = rows_expected / 24
            rows_expected += 1
            #print("Expected rows: %d" % rows_expected)
            #print("Available rows: %d" % result[0])
            if result[0] >= rows_expected:
                # fetch from cache
                self.cache.execute("SELECT dt, payload FROM values_%s WHERE dt >= ? AND dt <= ?" % resolution,
                [from_ts, to_ts])
                data = []
                for row in self.cache.fetchall():
                    data.append(pickle.loads(str(row[1])))
                return data
        # Cache missed or inactive.
        # Fetching a little more than required
        from_ts_request = from_ts
        to_ts_request = to_ts
        if resolution == 'hour':
            if (to_ts - from_ts) < (60 * 60 * 24):
                from_date_request = from_date.replace(hour=0, minute=0, second=0)
                from_ts_request = from_date_request.strftime('%s')
                to_date_request = from_date_request + timedelta(hours=24)
                to_ts_request = to_date_request.strftime('%s')
                #print(from_date_request, to_date_request)

        url = (self.base_url +
            '/history/station?id=%d&type=%s&start=%s&end=%s'
            % (station_id, resolution, from_ts_request, to_ts_request))
        data = self.do_request(url)
        if data is not None:
            if 'list' in data:
                if self.cache:
                    for rec in data['list']:
                        self.cache.execute("INSERT OR IGNORE INTO values_%s VALUES (?, ?)"
                            % resolution, [rec['dt'], pickle.dumps(rec)])
                    self.cacheconn.commit()
                return data['list']
        else:
            # maybe handle the None case here? Exception?
            pass

    def do_request(self, url, retries=3):
        s = requests.Session()
        s.mount(self.base_url, HTTPAdapter(max_retries=retries))
        if self.verbose:
            print("Requesting %s" % url)
        request = requests.get(url)
        return request.json()


def flatten_dict(d, parent_key=''):
    """Recursively flatten a dict"""
    items = []
    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key).items())
        elif type(v) == list:
            for n in range(len(v)):
                mykey = "%s_%d" % (new_key, n)
                items.extend(flatten_dict(v[n], mykey).items())
        else:
            items.append((new_key, v))
    return dict(items)


def to_csv(d):
    """Turn data into CSV and return"""
    import csv
    from StringIO import StringIO
    # collect all field names
    fieldnames = set()
    flattened_records = []
    for record in d:
        record = flatten_dict(record)
        for field in record.keys():
            fieldnames.add(field)
        flattened_records.append(record)
    fieldnames = sorted(fieldnames)
    out = None
    csvfile = StringIO()
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)
    for record in flattened_records:
        row = []
        for field in fieldnames:
            if field in record:
                row.append(str(record[field]))
            else:
                row.append('')
        writer.writerow(row)
    out = csvfile.getvalue()
    csvfile.close()
    return out


def main():
    """Command line client mode"""
    import argparse
    import daterangestr
    import sys
    parser = argparse.ArgumentParser(description='Get weather information from OpenWeatherMap.')
    parser.add_argument('-s', '--station', dest='station_id', type=int, metavar='STATION',
                   help='Station ID to get information for')
    parser.add_argument('-d', '--date', dest='daterange',
                   help='Date range for historic data retrieval, as string YYYYMMDD-YYYYMMDD.')
    parser.add_argument('--csv', dest='csv', action='store_true',
                   default=False,
                   help='Use CSV as output format for historic values')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   default=False,
                   help='Enable verbose output')
    args = parser.parse_args()
    if args.station_id is None:
        sys.stderr.write("ERROR: No station ID given. Use -s parameter, e.g. -s 4885.\n")
        sys.exit(1)
    ow = OpenWeather(verbose=args.verbose)
    weather = None
    if args.daterange is not None:
        (from_date, to_date) = daterangestr.to_dates(args.daterange)
        weather = ow.get_historic_weather(
            station_id=args.station_id,
            from_date=from_date,
            to_date=to_date,
            resolution="hour")
        if args.csv:
            print(to_csv(weather))
        else:
            print(json.dumps(weather, indent=4, sort_keys=True))
    else:
        weather = ow.get_weather(args.station_id)
        print(json.dumps(flatten_dict(weather), indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
