import requests
import random

from northstar_cloud.common import logs as logging
from northstar_cloud.common import utils as c_utils

LOG = logging.getLogger(__name__)


class WeatherAlertHeadlines(object):
    def __init__(self, host, default_params):
        self.host = host
        self.default_params = default_params

    def request_options (self, lat, lon):
        url = self.host + '/v3/alerts/headlines'
        params = self.default_params()
        params['geocode'] = '{lat},{lon}'.format(lat=lat, lon=lon)
        params['format'] = 'json'
        return url, params

    def handle_response(self, res):
        details = []
        if res and res['alerts']:
            # loop through alerts
            for alert in res['alerts']:
                # check fields to decide if this alert is important to you.
                print(alert)
                if alert['severityCode'] <= 3 and alert['certaintyCode'] <= 3 and alert['urgencyCode'] <= 3:
                    details.append(alert['detailKey'])
                    print('weather-alert-headlines: returning {} alert(s) meeting threshold out of {} total'.format(
                        len(details), len(res['alerts'])))
        else:
            print('weather-alert-headlines: No alerts in area')
        # return the detail_key(s) for alerts you deemed important
        return details


class WeatherAlertDetails(object):
    def __init__(self, host, default_params):
        self.host = host
        self.default_params = default_params

    def request_options(self, detail_key):
        url = self.host + '/v3/alerts/detail'
        params = self.default_params()
        params['alertId'] = detail_key
        params['format'] = 'json'
        return url, params


    def handle_response(self, res):
        if res and res['alertDetail']:
            alert = res['alertDetail']
            # Main thing here that is not in the alert headline is the alert['texts'] array
            print('weather-alerts-detail: {}'.format(alert['headlineText']))
            if alert['texts']:
                for text in alert['texts']:
                    print(text['languageCode'])
                    print(text['instruction'])
                    print(text['overview'])
                    print(text['description'])
            else:
                print('weather-alerts-detail: No alert text available')
        else:
            print('weather-alerts-detail: No alert detail available')

class WeatherDailyForecast(object):
    def __init__(self, host, default_params):
        self.host = host
        self.default_params = default_params

    def request_options(self, lat, lon, days=3, units='m'):
        d = days if days in [3, 5, 7, 10, 15] else 3
        u = units if units in ['e', 'm', 'h', 's'] else 'm'
        url = self.host + '/v1/geocode/{lat}/{lon}/forecast/daily/{days}day.json'.format(lat=lat, lon=lon, days=d)
        params = self.default_params
        params['units'] = u
        return url, params

    def handle_response(self, res):
        if res and res['forecasts']:
            forecasts = res['forecasts']
            print('daily-forecast: returned {}-day forecast'.format(len(forecasts)))

            # each entry in the forecasts array corresponds to a daily forecast
            for index, daily in enumerate(forecasts):
                print('daily-forecast: day {} - High of {}, Low of {}'.format(index, daily['max_temp'], daily['min_temp']))
                print('daily-forecast: day {} - {}'.format(index, daily['narrative']))
        # additional entries include (but not limited to):
        # lunar_phase, sunrise, day['uv_index'], night['wdir'], etc
        else:
            print('daily-forecast: no daily forecast returned')
        return res


class WeatherTropicalForecast(object):
    def __init__(self, host, default_params):
        self.host = host
        self.default_params = default_params


    def request_options(self, basin='AL', units='m', nautical=True, source='all'):
        u = units if units in ['e', 'm', 'h', 's'] else 'm'
        url = self.host + '/v2/tropical/projectedpath'

        params = self.default_params()
        params['units'] = u
        params['basin'] = basin
        params['nautical'] = 'true' if nautical else 'false'
        params['source'] = source
        params['format'] = 'json'

        return url, params

    def handle_response(self, res):
        if res and res['advisoryinfo']:
            print('tropical-forecast-projected-path: returned {} advisory info'.format(len(res['advisoryinfo'])))
            for storm in res['advisoryinfo']:
                # the storm's storm_name, projectedpath, and projectedpath.heading objects are probably of interest
                print('tropical-forecast-projected-path: Advisoory for storm "{}" by "{}"'.
                      format(storm['storm_name'],
                             storm['source']))
                print('tropical-forecast-projected-path: {} - {}'.format(storm['storm_name'], storm['projectedpath']))
        else:
            print('tropical-forecast-projected-path: No advisory info available')


class WeatherPowerDisruption(object):
    def __init__(self, host, default_params):
        self.host = host
        self.default_params = default_params

    def request_options(self, lat, lon):
        url = self.host + '/v2/indices/powerDisruption/daypart/15day'
        params = self.default_params()
        params['geocode'] = '{lat},{lon}'.format(lat=lat, lon=lon)
        params['format'] = 'json'
        return url, params

    def handle_response(self, res):
        if res and res['powerDisruptionIndex12hour']:
            p = res['powerDisruptionIndex12hour']
            for i, disruptIndex in enumerate(p['powerDisruptionIndex']):
                print('severe-weather-power-disruption-index: {}: {}'.format(disruptIndex, p['powerDisruptionCategory'][i]))
        else:
            print('severe-weather-power-disruption-index: no power distruption info returned')


class IBMWeatherServices(object):
    def __init__(self):
        self.host = c_utils.get_weather_host()
        self.default_params = c_utils.get_default_params()

        self.alert_headlines = WeatherAlertHeadlines(self.host, self.default_params)
        self.alert_details = WeatherAlertDetails(self.host, self.default_params)
        self.dailyforecast = WeatherDailyForecast(self.host, self.default_params)
        self.tropical_forecast = WeatherTropicalForecast(self.host, self.default_params)
        self.power_disruption = WeatherPowerDisruption(self.host, self.default_params)
        self.request_headers = c_utils.request_headers()

    def handleFail(self, op, err):
        LOG.exception("IBMWeatherServices: Failed %s with status code %s", op, str(err.status_code))

    def get_daily_forecast(self, lat, lon, units='m'):
        url, params = self.dailyforecast.request_options(lat, lon)
        headers = self.request_headers

        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            self.dailyforecast.handle_response(r.json())
            return r.json()
        else:
            self.handleFail('get_daily_forecast', r)
        return {}

    def get_hourly_forecast(self, lat, lon, units='m'):
        LOG.info("IBMWeatherServices: get_hourly_forecast for "
                  "location lat: %s, lang: %s", lat, lon)

        # Currently selecting local dummy data once we convert
        # DarkSky data with Weather API data, enable
        # 'get_daily_forecast' method for this call

        fire_data_1 = c_utils.get_dummy_weather_with_fire_data()
        fire_data_2 = c_utils.get_dummy_weather_no_fire_data()

        random_list = [fire_data_1, fire_data_2]
        return random.choice(random_list)


    def get_alert_headlines(self, lat, lon):
        url, params = self.alert_headlines.request_options(lat, lon)
        headers = self.request_headers

        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            detailKeys = self.alert_headlines.handle_response(r.json())
            if detailKeys and len(detailKeys) > 0:
                for detailKey in detailKeys:
                    print('Detail key: ' + detailKey)
                    self.get_alert_details(detailKey)
        else:
            self.handleFail('get_alert_headlines', r)

    def get_alert_details(self, detail_key):
         url, params = self.alert_details.request_options(detail_key)
         headers = self.request_headers

         r = requests.get(url, params=params, headers=headers)
         if r.status_code == 200:
             self.alert_details.handle_response(r.json())
         else:
             self.handleFail('get_alert_details', r)

    def get_tropical_forecast(self, basin='AL', units='m', nautical=True, source='all'):
        url, params = self.tropical_forecast.request_options(basin, units, nautical, source)
        headers = self.request_headers()

        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            self.tropical_forecast.handle_response(r.json())
        else:
            self.handleFail('get_tropical_forecast', r)

    def get_severe_power_disruption(self, lat, lon):
        url, params = self.power_disruption.request_options(lat, lon)
        headers = self.request_headers()

        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            self.power_disruption.handle_response(r.json())
        else:
            self.handleFail('get_severe_power_disruption', r)
