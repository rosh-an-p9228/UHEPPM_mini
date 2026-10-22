from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.traffic_service import traffic_service

router = APIRouter(prefix="/api/traffic", tags=["Traffic"])

@router.get("/current")
async def get_current_traffic(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    return await traffic_service.get_traffic_for_location(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"],
        ambient_temp=loc["baseline_temp"]
    )

@router.get("/heat")
async def get_traffic_heat(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    res = await traffic_service.get_traffic_for_location(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"],
        ambient_temp=loc["baseline_temp"]
    )
    return {
        "location_id": loc["id"],
        "location_name": loc["name"],
        "traffic_heat_contribution": res.get("traffic_heat_contribution", 12.0),
        "traffic_heat_level": res.get("heat_contribution_level", "Moderate"),
        "congestion_pct": res.get("congestion_pct", 50.0),
        "estimated_vehicle_activity": "Active Arterial Grid",
        "methodology": "Combines idle friction, exhaust thermal rejection, and ambient atmospheric temperature",
        "data_label": res.get("data_label", "MODEL ESTIMATE"),
        "source": res.get("source", "TomTom / Traffic Flow Model"),
        "status": res.get("status", "NEAR_REAL_TIME")
    }

