#!/usr/bin/env python3
"""Read-only NWS forecasts. Copyright (c) 2026 Hanie Kang. MIT License."""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

CITIES = {'Los Angeles': (34.0522,-118.2437,'America/Los_Angeles'),
          'New York': (40.7128,-74.0060,'America/New_York'),
          'Seattle': (47.6062,-122.3321,'America/Los_Angeles')}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def validate_forecast_url(url):
    parsed=urllib.parse.urlsplit(url)
    if (parsed.scheme!='https' or parsed.netloc!='api.weather.gov' or parsed.query or parsed.fragment
            or not re.fullmatch(r'/gridpoints/[A-Z]{3}/\d+,\d+/forecast',parsed.path)):
        raise ValueError('Unexpected forecast endpoint')
    return url

def fetch(url):
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    request=urllib.request.Request(url,headers={'User-Agent':'nws-city-forecast/1.0 (educational read-only client)',
                                              'Accept':'application/geo+json'})
    with opener.open(request,timeout=20) as response:
        data=response.read(1048577)
    if len(data)>1048576: raise ValueError('Response too large')
    return json.loads(data)

def forecast(city):
    lat,lon,zone=CITIES[city]
    point=fetch(f'https://api.weather.gov/points/{lat},{lon}')
    url=validate_forecast_url(point['properties']['forecast'])
    data=fetch(url)['properties']
    fields=('name','startTime','endTime','temperature','temperatureUnit','windSpeed','windDirection',
            'shortForecast','detailedForecast','probabilityOfPrecipitation')
    return {'city':city,'timezone':zone,'data_type':'forecast_not_current_observation',
            'issued_at':data.get('generatedAt'),'source_url':url,
            'periods':[{k:p.get(k) for k in fields} for p in data['periods'][:6]]}

def self_test():
    assert validate_forecast_url('https://api.weather.gov/gridpoints/LOX/154,44/forecast')
    for value in ('https://evil.example/gridpoints/LOX/1,2/forecast',
                  'https://api.weather.gov@evil.example/gridpoints/LOX/1,2/forecast',
                  'http://api.weather.gov/gridpoints/LOX/1,2/forecast',
                  'https://api.weather.gov/gridpoints/LOX/1,2/forecast?secret=x'):
        try:validate_forecast_url(value)
        except ValueError:continue
        raise AssertionError('Unsafe endpoint accepted')
    print('PASS: official endpoint accepted; four unsafe endpoints rejected; no network used.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--city',choices=sorted(CITIES),default='Los Angeles')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    if args.self_test:return self_test()
    try:print(json.dumps(forecast(args.city),ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,TypeError) as error:
        # Do not dump response content or environment variables.
        print(json.dumps({'error':'forecast_unavailable','error_type':type(error).__name__}),file=sys.stderr)
        raise SystemExit(1)
if __name__=='__main__':main()
