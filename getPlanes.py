#!/usr/bin/python
"""
How many planes are in the air?
Will they get grounded when everyone panics from COVID-19?
Let's find out.
Author: SJ Pratt
Date: 29 February 2020
"""

from opensky_api import OpenSkyApi as sky
import statistics as stat
import pandas as pd
import datetime as dt


epoch = dt.datetime.utcfromtimestamp(0)

def unixSecs(myTime):
    return (myTime - epoch).total_seconds()

def isNum(item):
    try:
        float(item)
        return True
    except:
        return False

def stats(vals):
    """
    Assumes vals is a list of numerics
    """
    rawLen = len(vals)
    vals = [x for x in vals if isNum(x)]
    minimum = min(vals)
    maximum = max(vals)
    n = len(vals)
    nans = rawLen - n
    mean = stat.mean(vals)
    median = stat.median(vals)
    return {'n':n, 'min':minimum, 'max':maximum, 'mean':mean, 'median':median, 'NaN': nans}

def makeDict(StateVector):
    """
    just ge the data back from the complicated object FFS
    """
    data = []       # empty list. Each element will be a dict
    for plane in StateVector:
        dic = plane.__dict__
        data.append(dic)
    return data

print("dude") 
#api = sky()
planes = sky().get_states().states

flying = [x for x in planes if not x.on_ground]

baroAlt = [x.baro_altitude for x in flying]

geoAlt = [x.geo_altitude for x in flying]
velocity = [x.velocity for x in flying]
verticalRate = [x.vertical_rate for x in flying if isNum(x.vertical_rate)]
ascending = [x for x in verticalRate if x > 0]
descending = [x for x in verticalRate if x < 0]
cruising = [x for x in verticalRate if x == 0]

baroAltStats = stats(baroAlt)
print('Planes: {}  Flying {}'.format(len(planes), len(flying)))
print("baro: ", baroAltStats)
print("geo Alt: ", stats(geoAlt))
print('vel: ', stats(velocity))
print('Ascending: ', stats(ascending))
print('Descending: ', stats(descending))
print('Cruising: ', stats(cruising))


#print(type(s))

planeDict = makeDict(planes)

planeFrame = pd.DataFrame.from_dict(planeDict)
planeFrame['timeStamp'] = "{:%Y%m%dT%H%M}".format(dt.datetime.now())

with open('covidPlanes.csv', 'a') as out:
    planeFrame.to_csv(out, mode = 'a', index = False, header = out.tell()==0)


#print(len(s))
#print(planes.states)


















