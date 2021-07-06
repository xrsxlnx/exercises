"""
The script is written by Ruslan Miriniuc 2021_06_24.
It retrieves weather data from https://openweathermap.org/ API using PyOWM library.
To run the script you should have an active API key, if not, register on openweathermap.org to get it.
Info about PyOWM library - https://pypi.org/project/pyowm/
"""

from pyowm import OWM

source = 'openweathermap'
owm = OWM(input('Enter your API key:'))
city = input('Enter a city name:')
mgr = owm.weather_manager()
observation = mgr.weather_at_place(city)
w = observation.weather
temp = w.temperature('celsius')['temp']
description = w.detailed_status
humidity = w.humidity

#print(w)

print('source={}, city="{}", description="{}", temp={}, humidity={}'
      .format(source, city, description, temp, humidity))

