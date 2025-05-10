import swisseph as swe
from dateutil import parser

ZODIAC_SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Список популярных неподвижных звёзд
FIXED_STAR_NAMES = [
    'Regulus', 'Spica', 'Sirius', 'Aldebaran', 'Antares',
    'Vega', 'Arcturus', 'Fomalhaut', 'Pollux', 'Castor',
    'Betelgeuse', 'Alphard', 'Deneb', 'Algol', 'Alcyone',
    'Dubhe', 'Acubens', 'Altair', 'Hamal', 'Rasalhague'
]


def degree_to_sign(degree):
    index = int(degree // 30) % 12
    sign_degree = degree % 30
    return ZODIAC_SIGNS[index], sign_degree


def calculate_star_positions(date_str, time_str):
    try:
        dt = parser.parse(f"{date_str} {time_str}")
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
        swe.set_ephe_path('.')  # для hosted server можно не задавать

        results = []
        for name in FIXED_STAR_NAMES:
            try:
                (lon, lat, dist), _ = swe.fixstar(name, jd)
                sign, deg = degree_to_sign(lon)
                results.append({
                    'star': name,
                    'degree': round(lon, 4),
                    'sign': sign,
                    'zodiac_degree': round(deg, 4)
                })
            except Exception as e:
                results.append({
                    'star': name,
                    'error': f"Не удалось получить: {str(e)}"
                })

        return {
            'mode': 'astro',
            'stars': results,
            'message': '✨ Положение 20+ неподвижных звёзд рассчитано'
        }

    except Exception as e:
        return {
            'error': f"Ошибка при расчёте звёзд: {str(e)}",
            'mode': 'error'
        }
