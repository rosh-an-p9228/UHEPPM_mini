from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from ..seed_data.seed_cities import resolve_location
from ..services.vegetation_service import vegetation_service
from ..services.satellite_service import satellite_service
from ..services.traffic_service import traffic_service

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/")
async def get_prevention_recommendations(location_id: Optional[str] = Query(None), category: Optional[str] = None, lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    loc = resolve_location(location_id=location_id, lat=lat, lon=lon)
    
    vegetation = vegetation_service.get_vegetation_metrics(loc["id"], loc["name"])
    satellite = satellite_service.get_satellite_lst(loc["id"], loc["name"])
    traffic = await traffic_service.get_traffic_for_location(loc["id"], loc["latitude"], loc["longitude"], loc["name"])
    
    all_recs = [
        {
            "id": "rec_veg_1",
            "category": "Vegetation",
            "title": "Municipal Tree Canopy & Green Corridors",
            "reason": f"Current NDVI is {vegetation['ndvi']} (Green cover: {vegetation['green_cover_pct']}%, Target gap: {vegetation['gap_pct']}%).",
            "priority": "HIGH",
            "expected_temp_reduction_range": "1.2°C – 2.5°C",
            "expected_temp_reduction_min": 1.2,
            "expected_temp_reduction_max": 2.5,
            "expected_risk_reduction": 18.5,
            "implementation_difficulty": "Moderate",
            "cost_category": "Moderate ($$)",
            "status": "Recommended",
            "action_steps": [
                "Deploy native shade trees (Neem, Peepal, Banyan, Gulmohar) along transit arteries.",
                "Target vacant municipal medians and civic school perimeters.",
                "Implement smart drip micro-irrigation using treated recycled municipal wastewater."
            ]
        },
        {
            "id": "rec_build_1",
            "category": "Buildings",
            "title": "High-Albedo Cool Roof Coating Mandate",
            "reason": f"Satellite thermal footprint shows surface radiative temperature reaching {satellite['lst_day']}°C on built concrete.",
            "priority": "HIGH",
            "expected_temp_reduction_range": "1.5°C – 2.8°C",
            "expected_temp_reduction_min": 1.5,
            "expected_temp_reduction_max": 2.8,
            "expected_risk_reduction": 22.0,
            "implementation_difficulty": "Easy",
            "cost_category": "Low ($)",
            "status": "Recommended",
            "action_steps": [
                "Apply solar-reflective elastomeric white paint (SRI > 82) to residential and commercial flat roofs.",
                "Incentivize commercial warehouses and IT parks with municipal green tax rebates.",
                "Reduces indoor thermal heat transfer by up to 4.5°C, lowering HVAC loads."
            ]
        },
        {
            "id": "rec_traffic_1",
            "category": "Traffic",
            "title": "Corridor Congestion De-bottlenecking & Idle Reduction",
            "reason": f"TomTom traffic flow shows {traffic['congestion_pct']}% congestion, releasing high vehicular combustion heat.",
            "priority": "MEDIUM",
            "expected_temp_reduction_range": "0.5°C – 1.2°C",
            "expected_temp_reduction_min": 0.5,
            "expected_temp_reduction_max": 1.2,
            "expected_risk_reduction": 12.0,
            "implementation_difficulty": "Moderate",
            "cost_category": "Moderate ($$)",
            "status": "Recommended",
            "action_steps": [
                "Implement adaptive signal timing to eliminate idling queues during 11:00-16:00 peak heat hours.",
                "Divert heavy freight traffic away from narrow urban residential street corridors.",
                "Expand shaded electric bus feeder routes."
            ]
        },
        {
            "id": "rec_health_1",
            "category": "Public Health",
            "title": "Emergency Cooling Shelters & Water Misting Kiosks",
            "reason": "Protect outdoor laborers, elderly citizens, and transit commuters from acute heat entrapment.",
            "priority": "CRITICAL",
            "expected_temp_reduction_range": "Immediate Direct Relief",
            "expected_temp_reduction_min": 3.0,
            "expected_temp_reduction_max": 6.0,
            "expected_risk_reduction": 25.0,
            "implementation_difficulty": "Easy",
            "cost_category": "Low ($)",
            "status": "Active Advisory",
            "action_steps": [
                "Convert public transit waiting hubs into air-cooled / shaded relief stations.",
                "Install solar-powered ultrasonic water misting lines along pedestrian promenades.",
                "Deploy mobile hydration tankers across outdoor construction and market zones."
            ]
        },
        {
            "id": "rec_urban_1",
            "category": "Urban Design",
            "title": "Permeable Pavements & Bioswale Water Channels",
            "reason": "High impervious asphalt fraction absorbs solar radiation and prevents natural ground moisture evaporative cooling.",
            "priority": "MEDIUM",
            "expected_temp_reduction_range": "0.8°C – 1.6°C",
            "expected_temp_reduction_min": 0.8,
            "expected_temp_reduction_max": 1.6,
            "expected_risk_reduction": 14.0,
            "implementation_difficulty": "Complex",
            "cost_category": "High ($$$)",
            "status": "Planned",
            "action_steps": [
                "Replace solid concrete parking lots with interlocking porous pavers.",
                "Construct roadside bioswales to capture storm runoff and sustain microclimate moisture."
            ]
        }
    ]
    
    if category and category != "all":
        all_recs = [r for r in all_recs if r["category"].lower() == category.lower()]
        
    return {
        "location_id": loc["id"],
        "location_name": loc["name"],
        "total_recommendations": len(all_recs),
        "recommendations": all_recs,
        "data_honesty_note": "Expected temperature reductions are empirical ranges derived from published urban climatology studies (Oke et al., Santamouris et al.)."
    }
