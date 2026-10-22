from fastapi import APIRouter, Query
from typing import Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.weather_service import weather_service
from ..services.traffic_service import traffic_service
from ..services.satellite_service import satellite_service
from ..services.vegetation_service import vegetation_service
from ..services.pollution_service import pollution_service
from ..services.population_service import population_service
from ..ml.heat_model import heat_model
from ..ml.hotspot_clustering import hotspot_engine

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/")
async def get_dashboard_summary(location_id: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    
    # 1. Fetch live/fallback weather
    weather = await weather_service.get_weather_for_location(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"]
    )
    
    # 2. Fetch traffic & vehicle heat
    traffic = await traffic_service.get_traffic_for_location(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"],
        ambient_temp=weather["temperature"]
    )
    
    # 3. Satellite LST
    satellite = satellite_service.get_satellite_lst(loc["id"], loc["name"])
    
    # 4. Vegetation / NDVI
    vegetation = vegetation_service.get_vegetation_metrics(loc["id"], loc["name"])
    
    # 5. Air Quality
    air_quality = await pollution_service.get_air_quality(
        location_id=loc["id"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        location_name=loc["name"]
    )
    
    # 6. Population & Urban Activity
    population = population_service.get_population_and_urban_density(loc["id"], loc["name"])
    
    # 7. AI Multi-Horizon Prediction & Heat Risk Index
    ai_prediction = heat_model.predict_multi_horizon(
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
    
    # 8. Hotspot Clustering
    hotspots = hotspot_engine.detect_hotspots(
        location_id=loc["id"],
        location_name=loc["name"],
        center_lat=loc["latitude"],
        center_lon=loc["longitude"],
        baseline_temp=weather["temperature"]
    )
    
    # 9. Top Action Recommendations
    top_recommendations = [
        {
            "id": "rec_1",
            "title": "Urban Canopy Corridor Planting",
            "category": "Vegetation",
            "priority": "HIGH" if vegetation["gap_pct"] > 10 else "MEDIUM",
            "reason": f"Green cover is only {vegetation['green_cover_pct']}% (Target: 30%, Gap: {vegetation['gap_pct']}%).",
            "expected_temp_reduction": "1.2°C – 2.4°C",
            "cost": "Moderate",
            "difficulty": "Easy to Moderate"
        },
        {
            "id": "rec_2",
            "title": "Cool Roofs & High-Albedo Facade Coating",
            "category": "Buildings",
            "priority": "HIGH" if satellite["lst_day"] >= 43.0 else "MEDIUM",
            "reason": f"High radiative surface temperature (LST: {satellite['lst_day']}°C) on concrete rooftops.",
            "expected_temp_reduction": "1.5°C – 2.8°C",
            "cost": "Low to Moderate",
            "difficulty": "Easy"
        },
        {
            "id": "rec_3",
            "title": "Arterial Congestion & Idle Suppression",
            "category": "Traffic",
            "priority": "HIGH" if traffic["congestion_pct"] > 70 else "MEDIUM",
            "reason": f"Peak vehicle congestion is at {traffic['congestion_pct']}%, causing significant thermal exhaust.",
            "expected_temp_reduction": "0.6°C – 1.1°C",
            "cost": "Moderate",
            "difficulty": "Moderate"
        },
        {
            "id": "rec_4",
            "title": "Public Hydration & Shade Corridors",
            "category": "Public Health",
            "priority": "CRITICAL" if ai_prediction["current_risk_score"] > 80 else "HIGH",
            "reason": f"Extreme Heat Risk Index ({ai_prediction['current_risk_score']}/100) affecting {population['baseline_population']:,} residents.",
            "expected_temp_reduction": "Direct Thermal Relief",
            "cost": "Low",
            "difficulty": "Immediate"
        }
    ]
    
    # 10. Heatwave Alert Status
    heatwave_detected = ai_prediction["predictions"][-1]["predicted_temp"] >= 41.0 or weather["temperature"] >= 38.0
    heatwave_alert = {
        "is_active": heatwave_detected,
        "title": "POTENTIAL HEATWAVE DETECTED" if heatwave_detected else "Normal Seasonal Thermal State",
        "severity": "CRITICAL" if weather["temperature"] >= 40.0 else ("High" if heatwave_detected else "Information"),
        "expected_duration_days": 3,
        "max_predicted_temp": round(max(p["predicted_temp"] for p in ai_prediction["predictions"]), 1),
        "advisory": "Avoid strenuous outdoor labor between 12:00 PM and 4:00 PM. Activate municipal cooling stations and hydration kiosks."
    }
    
    return {
        "location": loc,
        "kpi": {
            "temperature": weather["temperature"],
            "feels_like": weather["feels_like"],
            "aqi": air_quality["aqi"],
            "aqi_category": air_quality["category"],
            "heat_risk_score": ai_prediction["current_risk_score"],
            "heat_risk_category": ai_prediction["current_risk_category"],
            "predicted_temp_next_hour": ai_prediction["predictions"][1]["predicted_temp"],
            "predicted_temp_peak": round(max(p["predicted_temp"] for p in ai_prediction["predictions"]), 1),
            "green_cover_pct": vegetation["green_cover_pct"],
            "ndvi": vegetation["ndvi"],
            "traffic_congestion_pct": traffic["congestion_pct"],
            "traffic_heat_contribution": traffic["traffic_heat_contribution"],
            "population_density": population["population_density_per_sq_km"],
            "lst_day": satellite["lst_day"],
            "delta_from_previous_hour": "+0.8"
        },
        "weather": weather,
        "satellite": satellite,
        "vegetation": vegetation,
        "traffic": traffic,
        "air_quality": air_quality,
        "population": population,
        "ai_prediction": ai_prediction,
        "hotspots": hotspots,
        "recommendations": top_recommendations,
        "heatwave_alert": heatwave_alert,
        "data_transparency": {
            "weather_source": weather["source"],
            "satellite_source": satellite["sensor"],
            "ndvi_source": vegetation["sensor"],
            "traffic_source": traffic["source"],
            "population_source": population["data_source"],
            "air_quality_source": air_quality["source"]
        }
    }
