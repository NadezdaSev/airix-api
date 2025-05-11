from fastapi import FastAPI, Request
from astro_calc import calculate_natal
from stars_calc import parse_stars

app = FastAPI()

@app.post("/natal")
async def natal_chart(data: dict):
    try:
        birth_date = data.get('birth_date')
        birth_time = data.get('birth_time')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        result = calculate_natal(birth_date, birth_time, latitude, longitude)
        stars = parse_stars("sefstars.txt")
        result["stars"] = stars
        return result
    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

@app.get("/stars")
def get_stars():
    try:
        stars = parse_stars("sefstars.txt")
        return {"stars": stars}
    except Exception as e:
        return {"error": str(e)}
