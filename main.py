from fastapi import FastAPI, Request
from astro_calc import calculate_natal
from stars_calc import parse_stars  # 👈 добавляем импорт

app = FastAPI()


@app.post("/natal")
async def natal_chart(request: Request):
    data = await request.json()

    birth_date = data.get("birth_date")
    birth_time = data.get("birth_time")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    timezone = data.get("timezone")

    result = calculate_natal(birth_date, birth_time, latitude, longitude, timezone)

    # 👇 Вставка блока с неподвижными звёздами
    result["stars"] = parse_stars("sefstars.txt")

    return result
