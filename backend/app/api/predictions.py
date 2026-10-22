from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..ml.heat_model import heat_model
from ..services.weather_service import weather_service
from ..services.satellite_service import satellite_service
from ..services.vegetation_service import vegetation_service
from ..services.traffic_service import traffic_service
from ..services.pollution_service import pollution_service
from ..services.population_service import population_service

router = APIRouter(prefix="/api/predictions", tags=["AI Predictions"])

@router.get("/")
async def get_ai_predictions(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    
    weather = await weather_service.get_weather_for_location(loc["id"], loc["latitude"], loc["longitude"], loc["name"])
    satellite = satellite_service.get_satellite_lst(loc["id"], loc["name"])
    vegetation = vegetation_service.get_vegetation_metrics(loc["id"], loc["name"])
    traffic = await traffic_service.get_traffic_for_location(loc["id"], loc["latitude"], loc["longitude"], loc["name"], weather["temperature"])
    air_quality = await pollution_service.get_air_quality(lat=loc["latitude"], lng=loc["longitude"], location_id=loc["id"])
    population = population_service.get_population_and_urban_density(loc["id"], loc["name"])
    
    return heat_model.predict_multi_horizon(
        location_id=loc["id"],
        location_name=loc["name"],
        current_temp=weather["temperature"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
        uv_index=weather["uv_index"],
        lst=satellite["lst_day"],
        ndvi=vegetation["ndvi"],
        congestion_index=traffic["congestion_index"],
        traffic_heat=traffic["traffic_heat_contribution"],
        aqi=air_quality["aqi"],
        pop_density=population["population_density_per_sq_km"]
    )

