from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from ..seed_data.seed_cities import resolve_location

router = APIRouter(prefix="/api/heatwave", tags=["Heatwave Forecast"])

@router.get("/")
async def get_heatwave_forecast(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    base_temp = loc["baseline_temp"]
    
    is_heatwave = base_temp >= 38.0
    now = datetime.now(timezone.utc)
    
    forecast_days = [
        {
            "day": "Today",
            "date": (now).strftime("%b %d"),
            "max_temp": round(base_temp, 1),
            "min_temp": round(base_temp - 11.5, 1),
            "humidity_avg": loc["baseline_humidity"],
            "heat_index": round(base_temp + 3.2, 1),
            "status": "EXTREME HEAT" if base_temp >= 39.0 else "HIGH HEAT",
            "risk_color": "#ef4444" if base_temp >= 39.0 else "#f97316"
        },
        {
            "day": "Tomorrow",
            "date": (now + timedelta(days=1)).strftime("%b %d"),
            "max_temp": round(base_temp + 1.2, 1),
            "min_temp": round(base_temp - 10.8, 1),
            "humidity_avg": loc["baseline_humidity"] - 2.0,
            "heat_index": round(base_temp + 4.6, 1),
            "status": "HEATWAVE PEAK",
            "risk_color": "#ef4444"
        },
        {
            "day": "Day 3",
            "date": (now + timedelta(days=2)).strftime("%b %d"),
            "max_temp": round(base_temp + 0.8, 1),
            "min_temp": round(base_temp - 11.0, 1),
            "humidity_avg": loc["baseline_humidity"],
            "heat_index": round(base_temp + 4.0, 1),
            "status": "HEATWAVE CONTINUES",
            "risk_color": "#ef4444"
        },
        {
            "day": "Day 4",
            "date": (now + timedelta(days=3)).strftime("%b %d"),
            "max_temp": round(base_temp - 1.5, 1),
            "min_temp": round(base_temp - 12.0, 1),
            "humidity_avg": loc["baseline_humidity"] + 4.0,
            "heat_index": round(base_temp + 1.2, 1),
            "status": "MODERATE RISK",
            "risk_color": "#f59e0b"
        },
        {
            "day": "Day 5",
            "date": (now + timedelta(days=4)).strftime("%b %d"),
            "max_temp": round(base_temp - 2.4, 1),
            "min_temp": round(base_temp - 12.5, 1),
            "humidity_avg": loc["baseline_humidity"] + 6.0,
            "heat_index": round(base_temp - 0.5, 1),
            "status": "SAFE / NORMAL",
            "risk_color": "#10b981"
        }
    ]
    
    return {
        "location_id": loc["id"],
        "location_name": loc["name"],
        "heatwave_detected": is_heatwave,
        "alert_level": "RED (Severe Heatwave Warning)" if is_heatwave else "YELLOW (Watch)",
        "expected_duration_days": 3 if is_heatwave else 0,
        "max_predicted_temp": round(base_temp + 1.2, 1),
        "nighttime_thermal_minimum": round(base_temp - 10.8, 1),
        "high_nighttime_heat_flag": True if (base_temp - 10.8) >= 27.0 else False,
        "forecast_timeline": forecast_days,
        "vulnerable_population_impact": "High Risk for outdoor construction workers, elderly residents, and children.",
        "emergency_guidelines": [
            "Avoid direct sun exposure between 11:30 AM and 4:00 PM.",
            "Maintain continuous hydration with oral rehydration salts (ORS) or coconut water.",
            "Municipal health centers placed on high alert for heat exhaustion and heatstroke symptoms."
        ],
        "data_label": "Multi-day meteorological heatwave detection algorithm"
    }
