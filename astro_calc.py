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

    return f"{deg}{direction}{minutes:02d}"


def calculate_natal(date_str, time_str, lat, lon):
    try:
        parsed = parser.parse(f"{date_str} {time_str}")
        date_fmt = parsed.strftime("%Y/%m/%d")
        time_fmt = parsed.strftime("%H:%M")
        datetime = Datetime(date_fmt, time_fmt, '+03:00')  # Москва

        lat_str = to_dms_coord(lat, is_lat=True)
        lon_str = to_dms_coord(lon, is_lat=False)
        pos = GeoPos(lat_str, lon_str)

        chart = Chart(datetime, pos, hsys=const.HOUSES_PLACIDUS)

        planets = []
        for obj in PLANETS + ['CHIRON', 'LILITH', 'SELENA', 'MEAN_NODE', 'PARTFORTUNE']:
            try:
                planet = chart.get(obj)
                planets.append({
                    'name': planet.id,
                    'sign': planet.sign,
                    'degree': planet.lon,
                    'house': planet.house,
                })
            except Exception as e:
                print(f"Ошибка при расчёте объекта {obj}: {e}")

        return {
            'mode': 'astro',
            'planets': planets,
            'ASC': chart.get(const.ASC).sign,
            'MC': chart.get(const.MC).sign,
            'message': '⚙️ Астрологический расчёт выполнен',
        }

    except Exception as err:
        return {
            'error': f'Невозможно разобрать дату/время или координаты: {err}',
            'mode': 'error'
        }
