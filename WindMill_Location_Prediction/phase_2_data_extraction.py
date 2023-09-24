# -*- coding: utf-8 -*-
"""Phase 2 Data Extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RqhM20zoA5VaD6jNsVIco-z4C38Nymn-
"""

import requests
def getwaether(cor):
    api='30982862bf6ecbbbac2bfe22a3551a6c'
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=standard&appid={2}'.format(cor[0], cor[1], api)
    url = '    https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]'.format(cor[0], cor[1], api)

    weather_r=requests.get(url)
    weather_j=weather_r.json()
    return weather_j
lat= 18.5204
lon= 73.8567
c_weather = getwaether([lat,lon])
print(c_weather)

