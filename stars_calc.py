import os
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from dateutil import parser


STAR_FILE = 'sefstars.txt'
ORB_LIMIT = 1.0


def load_stars(filepath):
    stars = []
    if not os.path.isfile(filepath):
        return stars
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip() or '|' not in line:
                continue
            try:
                name, lon = line.strip().split('|')
                name = name.strip()
                lon = float(lon.strip())
                stars.append({'name': name, 'lon': lon})
            except Exception as e:
                print(f'Ошибка чтения строки: {line.strip()} — {e}')
    return stars


def calculate_star_links(date_str, time_str, lat, lon):
    try:
        parsed = parser.parse(f"{date_str} {time_str}")
        date_fmt = parsed.strftime("%Y/%m/%d")
        time_fmt = parsed.strftime("%H:%M")
        datetime = Datetime(date_fmt, time_fmt, '+03:00')
        pos = GeoPos(str(lat), str(lon))
        chart = Chart(datetime, pos, hsys=const.HOUSES_PLACIDUS)

        # Точки, с которыми сравниваем звезды
        points = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
                  const.JUPITER, const.SATURN, const.ASC, const.MC,
                  'CHIRON', 'LILITH', 'SELENA', 'MEAN_NODE', 'PARTFORTUNE']

        activated_stars = []
        stars = load_stars(STAR_FILE)

        for point in points:
            try:
                obj = chart.get(point)
                planet_lon = obj.lon
                for star in stars:
                    orb = abs((planet_lon - star['lon']) % 360)
                    if orb > 180:
                        orb = 360 - orb
                    if orb <= ORB_LIMIT:
                        activated_stars.append({
                            'name': star['name'],
                            'linked_to': point,
                            'orb': round(orb, 4)
                        })
            except Exception as e:
                print(f"⚠️ Ошибка при точке {point}: {e}")

        return {
            'mode': 'astro',
            'activated_stars': activated_stars,
            'message': '✨ Вычислены активные неподвижные звезды'
        }

    except Exception as err:
        return {
            'error': f"Ошибка расчета звёзд: {err}",
            'mode': 'error'
        }
