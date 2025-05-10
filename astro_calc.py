from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
]
POINTS = [const.ASC, const.MC, const.POF]

def calculate_natal(date_str, time_str, lat, lon):
    datetime = Datetime(date_str, time_str, '+00:00')
    pos = GeoPos(lat, lon)
    chart = Chart(datetime, pos, hsys='P')

    planets = []
    for obj in PLANETS + [POINTS.PartFortune, 'CHIRON', 'LILITH', 'SELENA', 'MEAN_NODE']:
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
        'ASC': chart.get('ASC').sign,
        'MC': chart.get('MC').sign,
        'message': '⚙️ Астрологический расчёт выполнен',
    }
