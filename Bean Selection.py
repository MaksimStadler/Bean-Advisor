# import required libraries
from datetime import *
from requests import *
import pandas as pd
from math import *
from bs4 import *

# set some variables
codeColumn = 'Code'
weather_dict = {}
weather_data = []

# load file data
icao_lut = pd.read_csv('station_lut.csv')
bean_lut = pd.read_csv('bean_lut.csv')
cloud_lut = pd.read_csv('cloud_lut.csv')
cloud_dict = cloud_lut.set_index('Code')['Value'].to_dict()
print(cloud_dict)

# Collect location/weather/time data
location_url = 'https://ipinfo.io'

location_data = eval(
    BeautifulSoup(get(location_url).text, 'lxml').select('p')[0].getText())

city = location_data['city'].upper()
country = location_data['country'].upper()
time = datetime.now()

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

print(weather_data)

# Determine Type of bean
for code in weather_data:
    if 'KT' in code:
        weather_dict['windSpeed'] = int(code[3:5])
    elif code[:3] in cloud_dict and 'sky' not in weather_dict:
        weather_dict['sky'] = cloud_dict[code[:3]]
    elif '/' in code:
        weather_dict['temperature'] = int(code.split('/')[0].replace('M', '-'))
        break

print(weather_dict)

bean_value = sum([weather_dict[key] for key in weather_dict]) % len()

# Determine quantity of bean

# Inform user or bean dose
