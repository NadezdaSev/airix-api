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
        datetime = Datetime(parsed.strftime("%Y/%m/%d"), parsed.strftime("%H:%M"), '+00:00')
        pos = GeoPos(lat, lon)
        chart = Chart(datetime, pos, hsys='P')

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
