from fastapi import FastAPI, Request
from astro_calc import calculate_natal
import yaml

app = FastAPI()

with open("airix_config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

@app.post("/natal")
async def natal_endpoint(request: Request):
    data = await request.json()
    if data.get("mode") == "semantic":
        return {
            "mode": "semantic",
            "message": "🧠 Семантический режим активен. Расчёт не выполняется.",
        }

    result = calculate_natal(
        date_str=data["birth_date"],
        time_str=data["birth_time"],
        lat=data["latitude"],
        lon=data["longitude"]
    )
    result["config_used"] = config.get("analysis_rules", {})
    return result
