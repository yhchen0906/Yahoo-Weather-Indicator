#! /usr/bin/env python
# -*- coding: utf-8 -*-
# file: weather.py
import argparse
import requests
locations, unit = [], ''
try:
    import config
except ImportError: pass
else:
    if 'LOCATION' in dir(config): locations = config.LOCATION
    if 'UNIT' in dir(config): unit = config.UNIT
parser = argparse.ArgumentParser(description = 'weather indicator')
parser.add_argument('-l', metavar = 'locations', help = 'locations (seperate by \',\' without blank space)')
parser.add_argument('-u', choices = ['c', 'C', 'f', 'F'], help = 'unit', metavar = 'unit')
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action = 'store_true', help = 'equal to -c -d 5')
group.add_argument('-c', action = 'store_true', help = 'current condition')
group.add_argument('-d', type = int, metavar = 'day', choices = [1, 2, 3, 4, 5], help = 'forecast')
parser.add_argument('-s', action = 'store_true', help = 'sunrise/sunset')
args = parser.parse_args()
if not (args.l or locations):
    parser.error('Must specify location')
if not (args.u or unit):
    parser.error('Must specify unit')
if not (args.a or args.c or args.d or args.s):
    parser.error('Must specify type of information')
if args.a: args.c, args.d = True, 5
if args.u: unit = args.u.lower()
if args.l: locations = args.l
UNIT = u'°' + unit.upper()
for location in locations.split(','):
    query = 'select * from weather.forecast where u="{}" and woeid in (select woeid from geo.places(1) where text="{}")'.format(unit, location)
    url = 'http://query.yahooapis.com/v1/public/yql?q={}&format=json'.format(query)
    data = requests.get(url).json()['query']['results']['channel']
    if args.c:
        condition = data['item']['condition']
        print data['location']['city'] + ', ' + condition['text'] + ', ' + condition['temp'] + UNIT
    if args.d:
        forecasts = data['item']['forecast']
        for forecast in forecasts[:args.d]:
            print forecast['date'], forecast['day'], forecast['low'] + UNIT, '~', forecast['high'] + UNIT, forecast['text']
    if args.s:
        astronomy = data['astronomy']
        print 'sunrise:', astronomy['sunrise'] + ', sunset:', astronomy['sunset']
