from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.satellite_service import satellite_service

router = APIRouter(prefix="/api/satellite", tags=["Satellite"])

@router.get("/lst")
async def get_satellite_lst(location_id: Optional[str] = Query(None), date: Optional[str] = None, lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    return satellite_service.get_satellite_lst(location_id=loc["id"], location_name=loc["name"], target_date=date)

