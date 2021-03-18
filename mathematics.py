import math


def to_rad(alpha):
    pi = math.atan(1) * 4
    alpha /= 180
    alpha *= pi
    return alpha


def to_deg(alpha):
    pi = math.atan(1) * 4
    alpha /= pi
    alpha *= 180
    return alpha


def rho(a, b, c, a1, b1, c1):
    d = -a ** 2 - b ** 2 - c ** 2
    dif = (a * a1 + b * b1 + c * c1 + d) / ((a ** 2 + b ** 2 + c ** 2) ** 0.5)
    return dif


def proekt(x0, y0, z0, xc, yc, zc):
    d = -x0 ** 2 - y0 ** 2 - z0 ** 2
    t = -(x0 * xc + y0 * yc + z0 * zc + d) / (x0 + y0 + z0)
    xp = xc + t
    yp = yc + t
    zp = zc + t
    return xp, yp, zp


def north(x0, y0, z0):
    d = -x0 ** 2 - y0 ** 2 - z0 ** 2
    xn = 0
    yn = 0
    zn = -d / z0
    return xn, yn, zn


def east(x0, y0, z0):
    d = -x0 ** 2 - y0 ** 2 - z0 ** 2
    xe = -d / x0
    ye = 0
    ze = 0
    return xe, ye, ze
