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

all_thetas = []
all_phis = []
all_times = []

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
    if theta >= 0:
        xn, yn, zn = north(x0, y0, z0)
        vec_nor = [xn - x0, yn - y0, zn - z0]
        len_nor = (vec_nor[0] ** 2 + vec_nor[1] ** 2 + vec_nor[2] ** 2) ** 0.5
        xp, yp, zp = proekt(x0, y0, z0, x, y, z)
        vec_pr = [xp - x0, yp - y0, zp - z0]
        len_pr = (vec_pr[0] ** 2 + vec_pr[1] ** 2 + vec_pr[2] ** 2) ** 0.5
        phi = math.acos((vec_nor[0] * vec_pr[0] + vec_nor[1] * vec_pr[1] + vec_nor[2] * vec_pr[2]) / (len_nor * len_pr))
        phi = to_deg(phi)

        xe, ye, ze = east(x0, y0, z0)
        x1 = vec_nor[0]
        y1 = vec_nor[1]
        z1 = vec_nor[2]
        vec_est = [y1 * z0 - z1 * y0,
                   -(x1 * z0 - x0 * z1),
                   x1 * y0 - y1 * x0]
        len_est = (vec_est[0] ** 2 + vec_est[1] ** 2 + vec_est[2] ** 2) ** 0.5
        phi1 = math.acos(
            (vec_est[0] * vec_pr[0] + vec_est[1] * vec_pr[1] + vec_est[2] * vec_pr[2]) / (len_est * len_pr))
        phi1 = to_deg(phi1)

        if phi1 > 90:
            phi = -phi + 360

    # print('theta =', theta, 'phi =', phi)
    all_thetas.append(theta)
    all_phis.append(phi)
    all_times.append(cur_time.copy())

events_thetas = []
events_phis = []
events_times = []

cur_event_thetas = []
cur_event_phis = []
cur_event_times = []
for i in range(len(all_thetas)):
    if all_thetas[i] >= 0:
        cur_event_thetas.append(all_thetas[i])
        cur_event_phis.append(to_rad(all_phis[i]))
        cur_event_times.append(all_times[i].copy())
    else:
        if cur_event_thetas:
            events_thetas.append(cur_event_thetas)
            events_phis.append(cur_event_phis)
            events_times.append(cur_event_times)
        cur_event_thetas = []
        cur_event_phis = []
        cur_event_times = []

for i in range(len(events_times)):
    print(events_times[i][0][0], events_times[i][0][1], events_times[i][0][2], sep='.', end=' ')
    print(events_times[i][0][3], events_times[i][0][4], sep=':', end=' ')
    print('Азимут:', str(to_deg(events_phis[i][0]))[:-12], 'градусов')

sf = plt.figure()
ax = sf.add_subplot(111, projection='3d')
ax.plot(dekart_coords_x, dekart_coords_y, dekart_coords_z)
ax.scatter(x0, y0, z0, color='red')
sf.set_size_inches(7, 7)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim(bottom=90, top=0)
for phi, theta in zip(events_phis, events_thetas):
    ax.plot(phi, theta)
fig.set_size_inches(7, 7)
plt.show()
