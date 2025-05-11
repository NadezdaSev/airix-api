from fastapi import FastAPI
from pydantic import BaseModel
from astro_calc import calculate_natal
from stars_calc import parse_stars

app = FastAPI()

class NatalData(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float

@app.get("/")
def root():
    return {"status": "Айрикс запущен и готов к работе"}

@app.post("/natal")
def natal_chart(data: NatalData):
    try:
        result = calculate_natal(data.birth_date, data.birth_time, data.latitude, data.longitude)
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