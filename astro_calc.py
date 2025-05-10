from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from dateutil import parser

PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
]
POINTS = [const.ASC, const.MC]


def to_dms_coord(value, is_lat=True):
    """Convert decimal degrees to DMS string like 55n45 or 37e37"""
    direction = ''
    deg = abs(int(float(value)))
    min_float = abs(float(value) - deg) * 60
    minutes = int(min_float)

    if is_lat:
        direction = 'n' if float(value) >= 0 else 's'
    else:
        direction = 'e' if float(value) >= 0 else 'w'

    return
