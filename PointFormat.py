import math as math


class PointCloud:
    def __init__(self):
        self.pointX = float()
        self.pointY = float()
        self.pointZ = float()
        self.velocity = float()
        self.sensorHeight = 2.1
        self.sensorElev = 15


def Spherical2Cartesian(r, a, e):
    x = r * math.cos(e) * math.sin(a)

    # y1 = r * math.cos(e) * math.cos(a)
    # z1 = r * math.sin(e)
    # y = y1 * math.cos(math.radians(0)) + z1 * math.sin(math.radians(0))
    # z = z1 * math.cos(math.radians(0)) - y1 * math.sin(math.radians(0)) + 2.1

    y = r * math.sin(e)
    z = 2.1 - r * math.cos(e) * math.cos(a)

    return x, y, z
