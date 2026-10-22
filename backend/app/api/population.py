from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.population_service import population_service

router = APIRouter(prefix="/api/population", tags=["Population"])

@router.get("/density")
async def get_population_density(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    return population_service.get_population_and_urban_density(location_id=loc["id"], location_name=loc["name"])

