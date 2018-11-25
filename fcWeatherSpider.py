#!/usr/bin/env python
#title           :weatherDataSpider.py
#description     :This will create a header for a python script.
#author          :Yuanyuan Zhao
#date            :20181003
#version         :1
#usage           :python pyscript.py
#notes           :
#python_version  :2.7.14
#==============================================================================
'''
    Access API to get weather data.
    path location correlation
    AUR02:41.796    -88.243 2/13-9/27
    CAR01:40.584    -74.243 2-26-9/27
    CHI01:41.853    -87.618 2/13-9/25
    FRA01:50.143    8.739   2/13-9/5
    SLO02:51.523    -0.636  2/13-9/5
    SEC10:40.777    -74.069 2/13-9/17
    TOR01:43.817    -79.339 2/13-9/27
    '''
from datetime import datetime, date, time, timedelta
import time as t1
import requests
import bs4
import json
from collections import OrderedDict
import yaml
import csv
from itertools import izip_longest
from itertools import chain
import csv

fmt = '%Y-%m-%d %H:%M:%S'

# paths and dates
# locs = [['AUR02', 41.796,-88.243],
#         ['CAR01', 40.584,-74.243],
#         ['CHI01', 41.853,-87.618],
#         ['FRA01', 50.143,8.739],
#         ['SLO02', 51.523,-0.636],
#         ['SEC10', 40.777,-74.069],
#         ['TOR01', 43.817,-79.339]]

# def timeSplitter(s, e, times):
#     while(s <= e):
#         temp = int(t1.mktime(t1.strptime(s.strftime(fmt), fmt)))
#         times.append(temp)
#         s = s + step


# step = timedelta(days=1)
# start1 = datetime.strptime('2018-2-12 00:00:00',fmt)
# end1 = datetime.strptime('2018-10-22 00:00:00',fmt)
# start2 = datetime.strptime('2018-2-12 23:00:00',fmt)
# end2 = datetime.strptime('2018-10-22 23:00:00',fmt)

# starts = timeSplitter(start1, end1, [])
# ends = timeSplitter(start2, end2, [])

filenames = ['AUR02-CAR01.csv', 'CHI02-AUR02.csv', 'FRA01-SLO02.csv', 'SEC10-TOR01.csv']

def spider(path):
    global fcResult
    fcResult = []
    locs = []
    with open(path, 'rb') as csvf:
        dataReader = csv.reader(csvf)
        for line in dataReader:
            locs.append(line)

    # savedFile = 'fcWeather_'+filenames[0]+'_'+locs[0][0]+'_'+locs[0][1]+'.csv'
    # f = csv.writer(open(savedFile, "wb+"))
    # f.writerow(["dt", "temp", "pressure", "humidity", "temp_min", "temp_max", "wind_speed", "wind_deg", "clouds", "weather"])
    for loc in locs:
        url = "http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&APPID=ea4985020f724407dea8833c9dfee64c"%(loc[0], loc[1])
        response = requests.get(url)
        json_data = yaml.load(json.dumps(response.json()))
        for x in json_data['list']:
            weather_data = ((item["id"], item["main"], item["description"]) for item in x["weather"])
            fcResult.append([datetime.utcfromtimestamp(int(x["dt"])).strftime('%Y-%m-%d %H:%M:%S'),
                        x["main"]["temp"],
                        x["main"]["pressure"],
                        x["main"]["humidity"],
                        x["main"]["temp_min"],
                        x["main"]["temp_max"],
                        x["wind"]["speed"],
                        x["wind"]["deg"],
                        x["clouds"]["all"],
                        list(weather_data)
                        ])
    return fcResult

fc_AUR02_CAR01 = spider('AUR02-CAR01.csv')
fc_CHI02_AUR02 = spider('CHI02-AUR02.csv')
fc_FRA01_SLO02 = spider('FRA01-SLO02.csv')
fc_SEC10_TOR01 = spider('SEC10-TOR01.csv')
