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

# epoch = dt.datetime.utcfromtimestamp(0)
#def unixSecs(myTime):
#    return (myTime - epoch).total_seconds()

def isNum(item):
    """
    Not used - exporting data to R
    """
    try:
        float(item)
        return True
    except:
        return False

def stats(vals):
    """
    Assumes vals is a list of numerics
    (I ended up not using this function - export data to csv and let R handle it)
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

def makeListofDicts(StateVector):
    """
    Just get the data back from the complicated object FFS
    """
    data = []       # empty list. Each element will be a dict
    for plane in StateVector:
        data.append(plane.__dict__)
    return data

planes = sky().get_states().states
planeDict = makeListofDicts(planes)
planeFrame = pd.DataFrame.from_dict(planeDict)
planeFrame['timeStamp'] = "{:%Y%m%dT%H%M}".format(dt.datetime.now())

with open('covidPlanes.csv', 'a') as out:
    planeFrame.to_csv(out, mode = 'a', index = False, header = out.tell()==0)

# Brief info for Journald
flying = [x for x in planes if not x.on_ground]
print('Planes: {}    Flying: {}'.format(len(planes), len(flying)))
