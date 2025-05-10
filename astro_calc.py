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

def calculate_natal(date_str, time_str, lat, lon):
    try:
        parsed = parser.parse(f"{date_str} {time_str}")
        date_fmt = parsed.strftime("%Y/%m/%d")
        time_fmt = parsed.strftime("%H:%M")
        datetime = Datetime(date_fmt, time_fmt, '+03:00')  # Москва
        pos = GeoPos(str(lat), str(lon))
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
            'error': f'Невозможно разобрать дату/время: {err}',
            'mode': 'error'
        }
