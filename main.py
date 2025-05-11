from fastapi import FastAPI, Request
from astro_calc import calculate_natal
from stars_calc import calculate_star_positions

app = FastAPI()


@app.post("/natal")
async def natal_chart(req: Request):
    data = await req.json()
    birth_date = data.get("birth_date")
    birth_time = data.get("birth_time")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    timezone = data.get("timezone")
    mode = data.get("mode", "astro")
    
    result = calculate_natal(birth_date, birth_time, latitude, longitude)
    result["mode"] = mode
    return result


@app.post("/stars")
async def stars_chart(req: Request):
    data = await req.json()
    birth_date = data.get("birth_date")
    birth_time = data.get("birth_time")
    return calculate_star_positions(birth_date, birth_time)
