from fastapi import APIRouter, Query
from typing import Dict, Any, List
from ..services.geocoding_service import geocoding_service
from ..database import get_db

router = APIRouter(prefix="/search", tags=["search"])

APP_PAGES = [
    {"title": "Global GIS Heat Map", "category": "Map & GIS", "tab": "heat_map", "description": "Interactive global Earth observation and satellite LST layer explorer."},
    {"title": "Urban Planning Scenario Simulator", "category": "Simulation", "tab": "simulation", "description": "Interactive dual-view microclimate intervention planning model."},
    {"title": "AI Heat Prediction Timeline", "category": "AI / ML", "tab": "prediction", "description": "Multi-horizon XGBoost thermal forecasting with 95% confidence intervals."},
    {"title": "Explainable AI (TreeSHAP)", "category": "AI / ML", "tab": "explainable_ai", "description": "Local feature attribution and physical heat entrapment drivers."},
    {"title": "NDVI & Green Canopy Deficit", "category": "Environment", "tab": "green_cover", "description": "Sentinel-2 multispectral vegetation index and canopy gap."},
    {"title": "Satellite Land Surface Temp (LST)", "category": "Satellite", "tab": "satellite", "description": "MODIS and Landsat 9 TIRS thermal infrared skin radiance."},
    {"title": "Traffic Flow & Combustion Heat", "category": "Urban", "tab": "traffic", "description": "Arterial congestion ratio and vehicular combustion heat estimation."},
    {"title": "Air Quality & Aerosol Entrapment", "category": "Environment", "tab": "air_quality", "description": "Continuous ambient CAAQMS / OpenAQ monitoring and radiation trapping."},
    {"title": "Carbon Reduction Calculator", "category": "Sustainability", "tab": "carbon", "description": "IPCC/EPA annual greenhouse gas offset and tree sequestration calculator."},
    {"title": "Street & Drone Image Heat Vision", "category": "Computer Vision", "tab": "image_analysis", "description": "Semantic photo segmentation and Visual Heat Exposure Score."},
    {"title": "Heatwave Early Warning Center", "category": "Alerts", "tab": "heatwave", "description": "Consecutive extreme diurnal temperature thresholds and advisories."},
    {"title": "Heat Vulnerability Assessment (HVI)", "category": "Vulnerability", "tab": "vulnerability", "description": "Socio-ecological hazard exposure, sensitivity, and coping capacity."},
    {"title": "Urban Climate AI Assistant", "category": "AI Assistant", "tab": "ai_assistant", "description": "Context-aware conversational decision support specialist."}
]

@router.get("/")
async def global_search(
    q: str = Query(..., min_length=1, description="Search query string")
) -> Dict[str, Any]:
    """
    Website-wide universal search across global places, addresses, application features,
    environmental indicators, and municipal records.
    """
    query = q.strip().lower()
    
    # 1. Matching application pages & features
    matched_pages = []
    for p in APP_PAGES:
        if query in p["title"].lower() or query in p["category"].lower() or query in p["description"].lower():
            matched_pages.append({
                "title": p["title"],
                "category": p["category"],
                "tab": p["tab"],
                "description": p["description"],
                "type": "feature"
            })

    # 2. Matching database seeded locations
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, city, state, latitude, longitude 
        FROM locations 
        WHERE LOWER(name) LIKE ? OR LOWER(city) LIKE ? OR LOWER(state) LIKE ?
        LIMIT 5
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    
    matched_locations = []
    for row in cursor.fetchall():
        matched_locations.append({
            "id": row[0],
            "title": f"{row[1]}, {row[2]}",
            "category": "Predefined Municipal Ward",
            "latitude": row[4],
            "longitude": row[5],
            "type": "location",
            "tab": "heat_map"
        })

    # 3. Global Places / Address Geocoding
    global_places = []
    try:
        places = await geocoding_service.forward_search(query)
        for pl in places:
            global_places.append({
                "title": pl["name"],
                "category": "Global Place / Address",
                "formatted_address": pl.get("formatted_address", ""),
                "latitude": pl["latitude"],
                "longitude": pl["longitude"],
                "type": "place",
                "tab": "heat_map"
            })
    except Exception as e:
        print(f"Global place search error: {e}")

    return {
        "query": q,
        "results": {
            "features": matched_pages,
            "monitored_wards": matched_locations,
            "global_places": global_places
        },
        "total_results": len(matched_pages) + len(matched_locations) + len(global_places)
    }
