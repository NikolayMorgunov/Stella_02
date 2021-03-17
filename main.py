import sgp4
from get_tle import *
import math
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from pyorbital.orbital import Orbital
import spacetrack
from get_diap import *
from next_time import *

TLE_FILE = "https://celestrak.com/NORAD/elements/active.txt"  # DB file to download
SAT_NAME = "NOAA 19                 "
# LK coords
LATITUDE = 55.93013
LONGITUDE = 37.51832
pi = math.atan(1) * 4

tle = from_strings(TLE_FILE, SAT_NAME)

diap = get_diap()

beg = diap[0]
end = diap[1]

cur_time = beg.copy()

while cur_time != end:
    cur_time_dt = dt.datetime(*cur_time)
    orb = Orbital("N", line1=tle[1], line2=tle[2])
    lon, lat, alt = orb.get_lonlatalt(cur_time_dt)
    print('lat =', lat, 'lon =', lon)
    cur_time = next_time(cur_time)
