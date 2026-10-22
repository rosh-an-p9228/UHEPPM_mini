from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.pollution_service import pollution_service

router = APIRouter(prefix="/api/air-quality", tags=["Air Quality"])

@router.get("/current")
async def get_current_air_quality(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    return await pollution_service.get_air_quality(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"]
    )

