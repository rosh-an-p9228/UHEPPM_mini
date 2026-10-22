from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.vegetation_service import vegetation_service

router = APIRouter(prefix="/api/vegetation", tags=["Vegetation"])

@router.get("/ndvi")
async def get_vegetation_ndvi(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    return vegetation_service.get_vegetation_metrics(location_id=loc["id"], location_name=loc["name"])

