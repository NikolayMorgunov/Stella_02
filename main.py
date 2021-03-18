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
from mathematics import *

TLE_FILE = "https://celestrak.com/NORAD/elements/active.txt"  # DB file to download
SAT_NAME = "NOAA 19                 "
# LK coords
LATITUDE = 55.93013
LONGITUDE = 37.51832
H = 0.2
Re = 6378.137
pi = math.atan(1) * 4
a0 = to_rad(LATITUDE)
b0 = to_rad(LONGITUDE)
r0 = Re + H
x0 = r0 * math.sin(a0) * math.cos(b0)
y0 = r0 * math.sin(a0) * math.sin(b0)
z0 = r0 * math.cos(a0)

tle = from_strings(TLE_FILE, SAT_NAME)

diap = get_diap()

beg = diap[0]
end = diap[1]

cur_time = beg.copy()
dekart_coords_x = []
dekart_coords_y = []
dekart_coords_z = []

while cur_time != end:
    cur_time_dt = dt.datetime(*cur_time)
    orb = Orbital("N", line1=tle[1], line2=tle[2])
    lon, lat, alt = orb.get_lonlatalt(cur_time_dt)
    a = to_rad(lon)
    b = to_rad(lat)
    r = alt + Re
    x = r * math.sin(a) * math.cos(b)
    y = r * math.sin(a) * math.sin(b)
    z = r * math.cos(a)
    dekart_coords_x.append(x)
    dekart_coords_y.append(y)
    dekart_coords_z.append(z)
    cur_time = next_time(cur_time)

    dist_to_fl = rho(x0, y0, z0, x, y, z)

    dist_to_sat = ((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) ** 0.5
    theta = math.asin(dist_to_fl / dist_to_sat)
    theta = to_deg(theta)
    phi = 0
    if theta >= 10:
        xn, yn, zn = north(x0, y0, z0)
        vec_nor = [xn - x0, yn - y0, zn - z0]
        len_nor = (vec_nor[0] ** 2 + vec_nor[1] ** 2 + vec_nor[2] ** 2) ** 0.5
        xp, yp, zp = proekt(x0, y0, z0, x, y, z)
        vec_pr = [xp - x0, yp - y0, zp - z0]
        len_pr = (vec_pr[0] ** 2 + vec_pr[1] ** 2 + vec_pr[2] ** 2) ** 0.5
        phi = math.acos((vec_nor[0] * vec_pr[0] + vec_nor[1] * vec_pr[1] + vec_nor[2] * vec_pr[2]) / (len_nor * len_pr))
        phi = to_deg(phi)

        xe, ye, ze = east(x0, y0, z0)
        vec_est = [xe - x0, ye - y0, ze - z0]
        len_est = (vec_est[0] ** 2 + vec_est[1] ** 2 + vec_est[2] ** 2) ** 0.5
        phi1 = math.acos((vec_est[0] * vec_pr[0] + vec_est[1] * vec_pr[1] + vec_est[2] * vec_pr[2]) / (len_est * len_pr))
        pli1 = to_deg(phi1)

        if (phi1 > 90):
           phi = -phi + 360

    print('theta =', theta, 'phi =', phi)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(dekart_coords_x, dekart_coords_y, dekart_coords_z)
ax.scatter(x0, y0, z0, color='red')
fig.set_size_inches(7, 7)
plt.show()
