#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:08:36 2018

@author: Phoebe
"""
import csv
import numpy as np
#from decimal import *
#getcontext().prec = 8

'''
processing of input feature
'''

idpath = "/Users/Phoebe/Desktop/data/"
idfile = "idList.csv"
idf = open(idpath+idfile,'r')

ids = {}
skip = True
key = 0
for line in idf:
    if skip:
        skip = False
        continue
    id = int(line.split(',')[0])
    ids[id] = key
    key += 1
print(ids)
print(len(ids))
    
totaloutput = []

#path = "/Users/Phoebe/Desktop/data/selected/AUR02-CAR01/"
#path = "/Users/Phoebe/Desktop/data/selected/CHI01-AUR02/"
#path = "/Users/Phoebe/Desktop/data/selected/FRA01-SLO02/"
#path = "/Users/Phoebe/Desktop/data/selected/SEC10-TOR01/"
#path = "/Users/Phoebe/Desktop/data/selected/AUR02-CHI01/"
#path = "/Users/Phoebe/Desktop/data/selected/CAR01-AUR02/"
path = "/Users/Phoebe/Desktop/data/selected/SLO02-FRA01/"

drpath = "/Users/Phoebe/Desktop/data/"
#drfile = "AUR02-CAR01.csv"
#drfile = "CHI01-AUR02.csv"
#drfile = "FRA01-SLO02.csv"
#drfile = "SEC10-TOR01.csv"
#drfile = "AUR02-CHI01.csv"
#drfile = "CAR01-AUR02.csv"
drfile = "SLO02-FRA01.csv"


#fields for a single location
#temp temp_diff pressure humidity wind_speed clouds bagofweathers
for i in range(10):
    filename = str(i) + ".csv"
    
    f = open(path+filename, 'r')
    reader = csv.reader(f)
    first = True
    
    output = []
    
    dates = []
    hours = []
    for line in reader:
        if first:
            first = False
            continue
        [date, time] = line[0].split(' ')
        hour = int(time.split(':')[0])
        if len(dates) != 0:
            if date == dates[-1]:
                interval = hour - hours[-1]
            else:
                interval = 24 + hour - hours[-1]
                if interval > 1:
                    print("other day!")#exam whether there are weather data missing between dates
            if interval > 1:
                prehour = hours[-1]
                for i in range(interval-1):#assume there are not weather data missing between dates
                    dates.append(date)
                    hours.append(prehour+i+1)
                    row = []
                    for j in range(len(ids)+6):
                        row.append(None)
                    output.append(row)
        temp_diff = float(line[5])-float(line[4])
        weather = []
        for i in range(len(ids)):
            weather.append(0)
        wtdata = line[9].split(')')
        for i in range(len(wtdata)-1):
            c = wtdata[i]
            c = c.split(", '")[0]
            wid = int(c.split('(')[1])
            weather[ids[wid]] = 1
        row = []
        row.append(float(line[1]))
        row.append(temp_diff)
        row.append(float(line[2]))
        row.append(float(line[3]))
        row.append(float(line[6]))
        row.append(float(line[8]))
        for i in range(len(weather)):
            row.append(weather[i])
        dates.append(date)
        hours.append(hour)
        output.append(row)
    print(len(dates), len(hours), len(output))
    print(len(output[0]))
    
    totaloutput.append(output)
    print(len(totaloutput))
    f.close()
    
totaloutput = np.hstack(totaloutput)
print(totaloutput.shape)


'''
processing of label

drop rate label correlation
0%           0
(0%,10%]     1
(10%,100%)   2
100%         3
'''
drfirst = True
drf = open(drpath+drfile, 'r')

drdate = []
drhour = []
dr = []

for line in drf:
    if drfirst:
        drfirst = False
        continue
    r = line.split(',')
    [date,time] = r[1].split('T')
    hour = int(time.split(':')[0])
    drdate.append(date)
    drhour.append(hour)
    dr.append(float(r[2]))      
drf.close()

#transfer from linear dr to catrgorical dr
def transfer(droprate):
    if droprate == 0:
        label = 0
    elif droprate <= 0.1:
        label = 1
    elif droprate < 1:
        label = 2
    elif droprate == 1:
        label = 3
    return label


#compute max, min, mean droprate
fdate = []
fhour = []
fdr = []
s = 0
total = dr[0]
maximum = dr[0]
minimum = dr[0]
for i in range(len(drhour)):
    if drhour[i] == drhour[i-1]:
        total += dr[i]
        maximum = np.max([maximum, dr[i]])
        minimum = np.min([minimum, dr[i]])
    if drhour[i] != drhour[i-1] and i != 0:
        fdate.append(drdate[i])
        fhour.append(drhour[i])
        meanlab = transfer(total/(i-s))
        maxlab = transfer(maximum)
        minlab = transfer(minimum)
#        fdr.append([total/(i-s), maximum, minimum])
        fdr.append([maxlab, meanlab, minlab])
        s = i
        total = dr[i]
        maximum = dr[i]
        minimum = dr[i]
print("length of hourly drop rate: ")
print(len(fdate), len(fhour), len(fdr))
#print(fdr[3])

'''
concate of weather data and drop rate data
'''
matched = []
index = 0
for i in range(len(dates)):
    if dates[i] == fdate[index] and hours[i] == fhour[index]:
#        print("matched!")
#        print(dates[i], hours[i])
        if None not in totaloutput[i]:
            row = np.append(totaloutput[i], fdr[index])
            matched.append(row)
        index = index + 1
    if index == len(fdr)-1:
        break
print("matched data shape: ")
print(len(matched), len(matched[0]))

print(len(dates), len(fdate), len(matched))

np.savetxt("/Users/Phoebe/Desktop/data/input/"+drfile, matched, delimiter=',', fmt = "%s")

    

    

    




















