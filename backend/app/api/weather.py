from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.weather_service import weather_service

router = APIRouter(prefix="/api/weather", tags=["Weather"])

@router.get("/current")
async def get_current_weather(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    return await weather_service.get_weather_for_location(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"]
    )

@router.get("/history")
async def get_weather_history(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    base_temp = loc["baseline_temp"]
    # 24-hour diurnal curve history
    history = []
    for h in range(24, 0, -2):
        hour_num = (14 - h) % 24
        factor = 2.8 if 12 <= hour_num <= 16 else (-2.2 if 2 <= hour_num <= 6 else 0.4)
        history.append({
            "hour": f"{hour_num:02d}:00",
            "temperature": round(base_temp + factor, 1),
            "humidity": round(loc["baseline_humidity"] - (factor * 2.2), 1),
            "heat_index": round(base_temp + factor + 2.5, 1)
        })
    return {"location_id": loc["id"], "location_name": loc["name"], "history": history}

