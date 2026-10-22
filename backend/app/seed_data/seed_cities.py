"""
Seed data providing high-resolution geospatial profiles, ward boundaries, and environmental baselines.
"""
from typing import Dict, Any, List, Optional
import math

CITIES_DATA: List[Dict[str, Any]] = [
    {
        "id": "nerul",
        "name": "Nerul (Sector 1-20)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0330,
        "longitude": 73.0297,
        "area_sq_km": 6.8,
        "baseline_population": 125000,
        "baseline_ndvi": 0.18,
        "baseline_lst": 44.2,
        "baseline_temp": 38.4,
        "baseline_humidity": 67.0,
        "baseline_aqi": 142,
        "baseline_traffic_congestion": 0.72,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [73.0180, 19.0450],
                [73.0420, 19.0420],
                [73.0450, 19.0220],
                [73.0210, 19.0200],
                [73.0180, 19.0450]
            ]]
        }
    },
    {
        "id": "belapur",
        "name": "CBD Belapur",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0180,
        "longitude": 73.0390,
        "area_sq_km": 5.4,
        "baseline_population": 95000,
        "baseline_ndvi": 0.28,
        "baseline_lst": 41.5,
        "baseline_temp": 36.8,
        "baseline_humidity": 69.0,
        "baseline_aqi": 115,
        "baseline_traffic_congestion": 0.58,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [73.0300, 19.0250],
                [73.0520, 19.0240],
                [73.0550, 19.0080],
                [73.0320, 19.0100],
                [73.0300, 19.0250]
            ]]
        }
    },
    {
        "id": "vashi",
        "name": "Vashi (Sector 9 & 17 / APMC)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0770,
        "longitude": 72.9980,
        "area_sq_km": 7.2,
        "baseline_population": 160000,
        "baseline_ndvi": 0.14,
        "baseline_lst": 45.8,
        "baseline_temp": 39.1,
        "baseline_humidity": 65.0,
        "baseline_aqi": 168,
        "baseline_traffic_congestion": 0.81,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [72.9850, 19.0880],
                [73.0120, 19.0850],
                [73.0100, 19.0650],
                [72.9860, 19.0680],
                [72.9850, 19.0880]
            ]]
        }
    },
    {
        "id": "kharghar",
        "name": "Kharghar (Sector 12 & Central Park)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0470,
        "longitude": 73.0690,
        "area_sq_km": 9.5,
        "baseline_population": 140000,
        "baseline_ndvi": 0.38,
        "baseline_lst": 39.8,
        "baseline_temp": 36.2,
        "baseline_humidity": 64.0,
        "baseline_aqi": 98,
        "baseline_traffic_congestion": 0.44,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [73.0550, 19.0600],
                [73.0850, 19.0580],
                [73.0820, 19.0320],
                [73.0520, 19.0350],
                [73.0550, 19.0600]
            ]]
        }
    },
    {
        "id": "airoli",
        "name": "Airoli (Mindspace Knowledge Park)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.1550,
        "longitude": 72.9980,
        "area_sq_km": 6.1,
        "baseline_population": 110000,
        "baseline_ndvi": 0.22,
        "baseline_lst": 43.1,
        "baseline_temp": 37.9,
        "baseline_humidity": 68.0,
        "baseline_aqi": 138,
        "baseline_traffic_congestion": 0.69,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [72.9850, 19.1680],
                [73.0120, 19.1650],
                [73.0100, 19.1420],
                [72.9860, 19.1450],
                [72.9850, 19.1680]
            ]]
        }
    },
    {
        "id": "ghansoli",
        "name": "Ghansoli (Industrial & RCP Zone)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.1250,
        "longitude": 73.0080,
        "area_sq_km": 5.8,
        "baseline_population": 98000,
        "baseline_ndvi": 0.16,
        "baseline_lst": 46.1,
        "baseline_temp": 39.4,
        "baseline_humidity": 63.0,
        "baseline_aqi": 175,
        "baseline_traffic_congestion": 0.76,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [72.9950, 19.1380],
                [73.0220, 19.1350],
                [73.0200, 19.1120],
                [72.9960, 19.1150],
                [72.9950, 19.1380]
            ]]
        }
    },
    {
        "id": "bandra_bkc",
        "name": "Bandra Kurla Complex (BKC)",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0660,
        "longitude": 72.8680,
        "area_sq_km": 4.5,
        "baseline_population": 180000,
        "baseline_ndvi": 0.11,
        "baseline_lst": 47.3,
        "baseline_temp": 39.8,
        "baseline_humidity": 72.0,
        "baseline_aqi": 182,
        "baseline_traffic_congestion": 0.88,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [72.8550, 19.0750],
                [72.8800, 19.0720],
                [72.8780, 19.0550],
                [72.8560, 19.0580],
                [72.8550, 19.0750]
            ]]
        }
    },
    {
        "id": "delhi_cp",
        "name": "Connaught Place / Central",
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "latitude": 28.6315,
        "longitude": 77.2167,
        "area_sq_km": 8.0,
        "baseline_population": 220000,
        "baseline_ndvi": 0.20,
        "baseline_lst": 48.5,
        "baseline_temp": 42.5,
        "baseline_humidity": 41.0,
        "baseline_aqi": 265,
        "baseline_traffic_congestion": 0.84,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [77.2050, 28.6420],
                [77.2300, 28.6400],
                [77.2280, 28.6200],
                [77.2060, 28.6220],
                [77.2050, 28.6420]
            ]]
        }
    },
    {
        "id": "bengaluru_ec",
        "name": "Electronic City Phase 1 & 2",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "latitude": 12.8399,
        "longitude": 77.6770,
        "area_sq_km": 11.2,
        "baseline_population": 130000,
        "baseline_ndvi": 0.26,
        "baseline_lst": 37.4,
        "baseline_temp": 34.2,
        "baseline_humidity": 58.0,
        "baseline_aqi": 88,
        "baseline_traffic_congestion": 0.70,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [77.6600, 12.8550],
                [77.6950, 12.8520],
                [77.6920, 12.8250],
                [77.6620, 12.8280],
                [77.6600, 12.8550]
            ]]
        }
    },
    {
        "id": "pune_hinjawadi",
        "name": "Hinjawadi IT Park Phase 1-3",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 18.5913,
        "longitude": 73.7389,
        "area_sq_km": 14.0,
        "baseline_population": 150000,
        "baseline_ndvi": 0.21,
        "baseline_lst": 42.0,
        "baseline_temp": 37.5,
        "baseline_humidity": 52.0,
        "baseline_aqi": 128,
        "baseline_traffic_congestion": 0.74,
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [73.7200, 18.6100],
                [73.7600, 18.6050],
                [73.7550, 18.5750],
                [73.7220, 18.5800],
                [73.7200, 18.6100]
            ]]
        }
    }
]

DYNAMIC_LOCATIONS: Dict[str, Dict[str, Any]] = {}

def register_dynamic_location(loc: Dict[str, Any]) -> Dict[str, Any]:
    """Registers a dynamically discovered or searched location into active memory."""
    if not loc or not loc.get("id"):
        return loc
    DYNAMIC_LOCATIONS[loc["id"]] = loc
    return loc

def resolve_location(location_id: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None) -> Dict[str, Any]:
    """
    Resolves any location_id (predefined ward or dynamic coordinate loc_lat_lon) or explicit (lat, lon)
    to a full geospatial profile.
    """
    # 1. Exact match in predefined CITIES_DATA
    if location_id:
        for c in CITIES_DATA:
            if c["id"].lower() == location_id.lower() or c["name"].lower() == location_id.lower():
                return c
                
    # 2. Check in DYNAMIC_LOCATIONS
    if location_id and location_id in DYNAMIC_LOCATIONS:
        return DYNAMIC_LOCATIONS[location_id]
        
    # 3. Parse coordinates from location_id if in format loc_19.0330_73.0297
    parsed_lat, parsed_lon = lat, lon
    if location_id and location_id.startswith("loc_"):
        parts = location_id[4:].split("_")
        if len(parts) >= 2:
            try:
                parsed_lat = float(parts[0])
                parsed_lon = float(parts[1])
            except ValueError:
                pass
                
    # 4. If coordinates are known, construct dynamic location
    if parsed_lat is not None and parsed_lon is not None:
        loc_key = f"loc_{parsed_lat:.4f}_{parsed_lon:.4f}"
        if loc_key in DYNAMIC_LOCATIONS:
            return DYNAMIC_LOCATIONS[loc_key]
            
        name = f"Coordinates ({parsed_lat:.3f}°, {parsed_lon:.3f}°)"
        city = "Urban Sector"
        state = "Regional Zone"
        country = "India" if (8.0 <= parsed_lat <= 37.0 and 68.0 <= parsed_lon <= 97.0) else "Global"
        base_temp = 36.5
        base_hum = 60.0
        base_lst = 42.0
        base_ndvi = 0.25
        base_aqi = 120
        base_traffic = 0.60
        
        for c in CITIES_DATA:
            dist = math.hypot(c["latitude"] - parsed_lat, c["longitude"] - parsed_lon)
            if dist < 0.05: # Within ~5km
                name = f"{c['name']} (Vicinity)"
                city = c["city"]
                state = c["state"]
                country = c["country"]
                base_temp = c["baseline_temp"]
                base_hum = c["baseline_humidity"]
                base_lst = c["baseline_lst"]
                base_ndvi = c["baseline_ndvi"]
                base_aqi = c["baseline_aqi"]
                base_traffic = c["baseline_traffic_congestion"]
                break

        dynamic_entry = {
            "id": loc_key,
            "name": name,
            "city": city,
            "state": state,
            "country": country,
            "latitude": parsed_lat,
            "longitude": parsed_lon,
            "area_sq_km": 6.0,
            "baseline_population": 110000,
            "baseline_ndvi": base_ndvi,
            "baseline_lst": base_lst,
            "baseline_temp": base_temp,
            "baseline_humidity": base_hum,
            "baseline_aqi": base_aqi,
            "baseline_traffic_congestion": base_traffic,
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[
                    [parsed_lon - 0.015, parsed_lat + 0.015],
                    [parsed_lon + 0.015, parsed_lat + 0.015],
                    [parsed_lon + 0.015, parsed_lat - 0.015],
                    [parsed_lon - 0.015, parsed_lat - 0.015],
                    [parsed_lon - 0.015, parsed_lat + 0.015]
                ]]
            }
        }
        DYNAMIC_LOCATIONS[loc_key] = dynamic_entry
        return dynamic_entry
        
    return CITIES_DATA[0]

