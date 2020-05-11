# import required libraries
from datetime import *
from requests import *
import pandas as pd
import numpy as np
from bs4 import *

print('Finding Location...')

# set some variables
codeColumn = 'Code'
weather_dict = {}
weather_data = []

# load file data
icao_lut = pd.read_csv('station_lut.csv')
bean_lut = pd.read_csv('bean_lut.csv')
bean_list = list(bean_lut['type'])
cloud_lut = pd.read_csv('cloud_lut.csv')
cloud_dict = cloud_lut.set_index('Code')['Value'].to_dict()

# Collect location/weather/time data
location_url = 'https://ipinfo.io'

location_data = eval(
    BeautifulSoup(get(location_url).text, 'lxml').select('p')[0].getText())

city = location_data['city'].upper()
country = location_data['country'].upper()
curr_time = datetime.now()

print('{}, {}'.format(city, country))
print('Chcecking the weather...')

try:
    # filter icao_lut based on country/city
    city_filter = icao_lut['City'].str.contains(city, na=False)
    country_filter = icao_lut['Country'] == country
    icao_list = list(icao_lut[country_filter][city_filter]['ICAO'])
    for icao in icao_list:
        weather_url = 'https://www.aviationweather.gov/metar/data?ids=' + icao
        weather_data = BeautifulSoup(get(weather_url).text, 'lxml').select(
            'code')
        # test for available weather data and record first available string
        if weather_data:
            weather_data = weather_data[0].getText().split(' ')
            break
except Exception:
    weather_data = []
    print('Your location could not be identified. No beans for you.')
    raise

# Determine Type of bean
for code in weather_data:
    if 'KT' in code:
        weather_dict['windSpeed'] = int(code[-4:-2])
    elif code[:3] in cloud_dict and 'sky' not in weather_dict:
        weather_dict['sky'] = cloud_dict[code[:3]]
    elif '/' in code:
        weather_dict['temperature'] = int(code.split('/')[0].replace('M', '-'))
        break

print('Done')

bean_value = (np.prod([weather_dict[k] for k in weather_dict]) / 2) % (
        len(bean_list) - 1)
bean_type = bean_list[int(bean_value)]

# Determine quantity of bean
bean_quantity = (curr_time.hour * curr_time.minute) % 60 + 1

# Inform user or bean dose
print('We recommend you consume {0} {1}.'.format(bean_quantity, bean_type))
