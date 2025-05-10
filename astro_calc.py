from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from dateutil import parser

PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
]

EXTRAS = ['CHIRON', 'LILITH', 'SELENA', 'MEAN_NODE', 'PARTFORTUNE']


def to_dms_coord(value, is_lat=True):
    deg = abs(int(float(value)))
    minutes = int(abs(float(value) - deg) * 60)
    direction = 'n' if is_lat and float(value) >= 0 else \
                's' if is_lat else \
                'e' if float(value) >= 0 else 'w'
    return f"{deg}{direction}{minutes:02d}"


def calculate_natal(date_str, time_str, lat, lon):
    try:
        parsed = parser.parse(f"{date_str} {time_str}")
        date_fmt = parsed.strftime("%Y/%m/%d")
        time_fmt = parsed.strftime("%H:%M")
        datetime = Datetime(date_fmt, time_fmt, '+03:00')
        pos = GeoPos(to_dms_coord(lat, True), to_dms_coord(lon, False))
        chart = Chart(datetime, pos, hsys=const.HOUSES_PLACIDUS)

        planets = []
        for obj in PLANETS + EXTRAS:
            try:
                planet = chart.get(obj)
                result = {
                    'name': planet.id,
                    'sign': planet.sign,
                    'degree': planet.lon
                }
                if hasattr(planet, 'house'):
                    result['house'] = getattr(planet, 'house', None)
                planets.append(result)
            except Exception as e:
                print(f"⚠️ Ошибка при обработке {obj}: {e}")

        return {
            'mode': 'astro',
            'planets': planets,
            'ASC': chart.get(const.ASC).sign,
            'MC': chart.get(const.MC).sign,
            'message': '⚙️ Астрологический расчёт выполнен',
        }

    except Exception as err:
        return {
            'error': f"Невозможно разобрать дату/время или координаты: {err}",
            'mode': 'error'
        }
