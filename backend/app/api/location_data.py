from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, Optional
import datetime
import asyncio

from ..services.geocoding_service import geocoding_service
from ..services.weather_service import weather_service
from ..services.earth_engine_service import earth_engine_service
from ..services.traffic_service import traffic_service
from ..services.pollution_service import pollution_service
from ..services.population_service import population_service
from ..ml.heat_model import heat_model
from ..ml.explain_shap import explain_shap
from ..config import settings
from ..seed_data.seed_cities import register_dynamic_location

router = APIRouter(prefix="/location-data", tags=["location-data"])

@router.get("/")
async def get_unified_location_data(
    lat: float = Query(..., description="Latitude coordinate between -90 and 90"),
    lng: float = Query(..., description="Longitude coordinate between -180 and 180"),
    date: Optional[str] = Query(None, description="Optional observation date YYYY-MM-DD")
) -> Dict[str, Any]:
    """
    Unified real-time dynamic intelligence endpoint for any coordinate on Earth.
    Orchestrates Geocoding, Weather, Satellite LST, Sentinel NDVI, Traffic, Air Quality,
    Population Density, XGBoost Forecasts, TreeSHAP Attributions, and Cooling Recommendations.
    """
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise HTTPException(status_code=400, detail="Invalid latitude or longitude range.")

    now = datetime.datetime.now(datetime.timezone.utc)

    # 1. Reverse geocoding
    geo = await geocoding_service.reverse_geocode(lat, lng)

    # 2. Parallel asynchronous fetching of environmental datasets
    weather_task = weather_service.get_current_weather(lat, lng, geo["name"])
    satellite_task = earth_engine_service.get_satellite_lst(lat, lng, date)
    vegetation_task = earth_engine_service.get_sentinel_ndvi(lat, lng)
    pollution_task = pollution_service.get_air_quality(lat, lng)
    population_task = population_service.get_population_profile(lat, lng)

    weather, satellite, vegetation, pollution, population = await asyncio.gather(
        weather_task, satellite_task, vegetation_task, pollution_task, population_task
    )

    # 3. Traffic data based on current temperature
    traffic = await traffic_service.get_traffic_heat(lat, lng, weather.get("temperature", 35.0))

    # 4. Multi-Horizon ML Prediction & Risk Index
    temp = weather.get("temperature", 35.0)
    humidity = weather.get("humidity", 60.0)
    wind_spd = weather.get("wind_speed", 3.5)
    uv = weather.get("uv_index", 7.0)
    lst = satellite.get("lst_day", 42.0)
    ndvi = vegetation.get("ndvi", 0.25)
    congestion_idx = traffic.get("congestion_index", 0.5)
    traf_heat = traffic.get("traffic_heat_contribution", 12.0)
    aqi_val = pollution.get("aqi", 120.0)
    pop_dens = population.get("population_density_per_sq_km", 12000.0)

    prediction_result = heat_model.predict_multi_horizon(
        location_id=geo.get("place_id", f"loc_{lat}_{lng}"),
        location_name=geo["name"],
        current_temp=temp,
        humidity=humidity,
        wind_speed=wind_spd,
        uv_index=uv,
        lst=lst,
        ndvi=ndvi,
        congestion_index=congestion_idx,
        traffic_heat=traf_heat,
        aqi=aqi_val,
        pop_density=pop_dens
    )

    # 5. TreeSHAP Feature Attributions
    shap_factors = explain_shap.generate_explanation(
        temp=temp,
        lst=lst,
        ndvi=ndvi,
        traffic_heat=traf_heat,
        aqi=aqi_val,
        pop_density=pop_dens,
        wind_speed=wind_spd
    )

    # 6. Socio-Ecological Vulnerability Assessment
    exposure_score = round(min(100.0, (temp * 1.5) + (lst * 0.8)), 1)
    sensitivity_score = round(min(100.0, (pop_dens / 250.0) + (aqi_val * 0.2)), 1)
    adaptive_capacity = round(max(5.0, (ndvi * 80.0) + 15.0), 1)
    hvi_score = round(min(100.0, max(10.0, (exposure_score * 0.45) + (sensitivity_score * 0.35) - (adaptive_capacity * 0.20))), 1)

    # 7. Targeted Cooling Recommendations
    recommendations = []
    if vegetation.get("gap_pct", 0) > 8.0:
        recommendations.append({
            "title": "Urban Canopy Corridor Expansion",
            "category": "Vegetation",
            "priority": "HIGH",
            "reason": f"Canopy deficit is {vegetation.get('gap_pct')}% below the 30% municipal buffer target.",
            "expected_temp_reduction": "1.2°C – 2.4°C",
            "cost": "Moderate",
            "difficulty": "Easy to Moderate"
        })
    if lst > 38.0:
        recommendations.append({
            "title": "High-Albedo Cool Roof & Pavement Retrofit",
            "category": "Buildings",
            "priority": "HIGH" if lst > 42.0 else "MEDIUM",
            "reason": f"Satellite thermal radiance reaches {lst}°C across impervious roofs.",
            "expected_temp_reduction": "1.5°C – 2.8°C",
            "cost": "Low to Moderate",
            "difficulty": "Easy"
        })
    if traffic.get("congestion_pct", 0) > 50.0:
        recommendations.append({
            "title": "Dynamic Traffic Flow Optimization",
            "category": "Traffic",
            "priority": "MEDIUM",
            "reason": f"Vehicular combustion heat contribution is +{traf_heat} pts.",
            "expected_temp_reduction": "0.5°C – 1.0°C",
            "cost": "Moderate",
            "difficulty": "Moderate"
        })
    if prediction_result.get("current_risk_score", 50) >= 75.0:
        recommendations.append({
            "title": "Civic Hydration & Cooling Shelters Activation",
            "category": "Public Health",
            "priority": "CRITICAL",
            "reason": "Heat Risk Index is in the EXTREME bracket for local residents.",
            "expected_temp_reduction": "Immediate Thermal Relief",
            "cost": "Low",
            "difficulty": "Immediate"
        })

    loc_id = f"loc_{lat:.4f}_{lng:.4f}"
    register_dynamic_location({
        "id": loc_id,
        "name": geo["name"],
        "city": geo["city"],
        "state": geo["state"],
        "country": geo["country"],
        "latitude": lat,
        "longitude": lng,
        "area_sq_km": population.get("area_sq_km", 5.2),
        "baseline_population": population.get("baseline_population", 100000),
        "baseline_ndvi": vegetation.get("ndvi", 0.25),
        "baseline_lst": satellite.get("lst_day", 42.0),
        "baseline_temp": weather.get("temperature", 35.0),
        "baseline_humidity": weather.get("humidity", 60.0),
        "baseline_aqi": int(pollution.get("aqi", 120)),
        "baseline_traffic_congestion": traffic.get("congestion_index", 0.5),
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [lng - 0.015, lat + 0.015],
                [lng + 0.015, lat + 0.015],
                [lng + 0.015, lat - 0.015],
                [lng - 0.015, lat - 0.015],
                [lng - 0.015, lat + 0.015]
            ]]
        }
    })

    return {
        "location": {
            "latitude": lat,
            "longitude": lng,
            "name": geo["name"],
            "city": geo["city"],
            "state": geo["state"],
            "country": geo["country"],
            "formatted_address": geo["formatted_address"],
            "source": geo["source"],
            "status": geo["status"]
        },
        "kpi": {
            "heat_risk_score": prediction_result["current_risk_score"],
            "heat_risk_category": prediction_result["current_risk_category"],
            "temperature": temp,
            "feels_like": weather.get("feels_like", temp + 2.5),
            "lst_day": lst,
            "green_cover_pct": vegetation.get("green_cover_pct", 20.0),
            "traffic_congestion_pct": traffic.get("congestion_pct", 50.0),
            "aqi": int(aqi_val),
            "hvi_score": hvi_score
        },
        "weather": weather,
        "satellite": satellite,
        "vegetation": vegetation,
        "traffic": traffic,
        "air_quality": pollution,
        "population": population,
        "ai_prediction": prediction_result,
        "explainable_ai": shap_factors,
        "vulnerability": {
            "overall_vulnerability_score": hvi_score,
            "vulnerability_category": "HIGH" if hvi_score >= 70 else ("MODERATE" if hvi_score >= 45 else "LOW"),
            "exposure_score": exposure_score,
            "sensitivity_score": sensitivity_score,
            "adaptive_capacity": adaptive_capacity
        },
        "recommendations": recommendations,
        "heatwave_alert": {
            "is_active": temp >= 40.0 or prediction_result["current_risk_score"] >= 80.0,
            "title": "EXTREME HEAT HAZARD WATCH" if temp >= 40.0 else "ADVISORY WATCH",
            "severity": "CRITICAL" if temp >= 42.0 else ("HIGH" if temp >= 40.0 else "MODERATE"),
            "max_predicted_temp": max([p["predicted_temp"] for p in prediction_result.get("predictions", [])] or [temp]),
            "expected_duration_days": 3 if temp >= 40.0 else 1,
            "advisory": "Avoid strenuous afternoon outdoor exertion. Maintain hydration and seek shaded or cooled public facilities."
        },
        "timestamps": {
            "requested_at": now.isoformat(),
            "data_freshness_seconds": 12
        }
    }

@router.get("/current")
async def get_current_location() -> Dict[str, Any]:
    """
    Returns the default/initial location for the website.
    This is used as the starting location when the website loads.
    """
    return {
        "latitude": settings.DEFAULT_LAT,
        "longitude": settings.DEFAULT_LON,
        "location_name": settings.DEFAULT_LOCATION_NAME,
        "source": "Default Configuration"
    }
