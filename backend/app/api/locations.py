from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..seed_data.seed_cities import CITIES_DATA, DYNAMIC_LOCATIONS, resolve_location

router = APIRouter(prefix="/api/locations", tags=["Locations"])

@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_locations():
    """Retrieve all monitored municipal wards and dynamically active urban regions"""
    active_dynamic = [loc for loc in DYNAMIC_LOCATIONS.values() if not any(c["id"] == loc["id"] for c in CITIES_DATA)]
    return active_dynamic + CITIES_DATA

@router.get("/{location_id}", response_model=Dict[str, Any])
async def get_location_by_id(location_id: str):
    """Retrieve detailed boundary and environmental baseline for a specific location or coordinate"""
    loc = resolve_location(location_id)
    if not loc:
        raise HTTPException(status_code=404, detail=f"Location {location_id} not found")
    return loc

