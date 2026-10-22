import httpx
import os
import math
from typing import Dict, Any, Optional
from ..config import settings
from ..seed_data.seed_cities import CITIES_DATA

class GeocodingService:
    def __init__(self):
        self.google_api_key = settings.GOOGLE_MAPS_API_KEY or os.getenv("GOOGLE_MAPS_API_KEY", "")

    async def reverse_geocode(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Reverse geocodes (lat, lng) to human readable address, city, state, country.
        1. Checks seeded municipal database first for instant sub-millisecond match.
        2. Queries Google Geocoding REST API if key exists.
        3. Queries OpenStreetMap Nominatim with fast 1.5s timeout.
        4. Geometric coordinate fallback.
        """
        # 1. Check seeded municipal wards first
        for loc in CITIES_DATA:
            d_lat = abs(loc["latitude"] - lat)
            d_lng = abs(loc["longitude"] - lng)
            if d_lat < 0.04 and d_lng < 0.04:
                return {
                    "formatted_address": f"{loc['name']}, {loc['city']}, {loc['state']}, India",
                    "name": loc["name"],
                    "city": loc["city"],
                    "state": loc["state"],
                    "country": "India",
                    "place_id": loc["id"],
                    "source": "Municipal GIS Geodatabase",
                    "status": "LIVE"
                }

        # 2. Try Google Geocoding REST API if key configured
        if self.google_api_key:
            try:
                async with httpx.AsyncClient(timeout=1.5) as client:
                    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={self.google_api_key}"
                    res = await client.get(url)
                    if res.status_code == 200:
                        data = res.json()
                        if data.get("status") == "OK" and data.get("results"):
                            top = data["results"][0]
                            comps = top.get("address_components", [])
                            
                            city = ""
                            state = ""
                            country = ""
                            neighborhood = ""
                            
                            for c in comps:
                                types = c.get("types", [])
                                if "locality" in types:
                                    city = c.get("long_name", "")
                                elif "sublocality" in types or "neighborhood" in types:
                                    if not neighborhood:
                                        neighborhood = c.get("long_name", "")
                                elif "administrative_area_level_1" in types:
                                    state = c.get("long_name", "")
                                elif "country" in types:
                                    country = c.get("long_name", "")
                                    
                            name = neighborhood or city or f"Sector ({lat:.3f}, {lng:.3f})"
                            
                            return {
                                "formatted_address": top.get("formatted_address", ""),
                                "name": name,
                                "city": city or neighborhood or "Urban Area",
                                "state": state or "Region",
                                "country": country or "Global",
                                "place_id": top.get("place_id", f"place_{lat}_{lng}"),
                                "source": "Google Geocoding API",
                                "status": "LIVE"
                            }
            except Exception as e:
                print(f"Google Geocoding error: {e}")

        # 3. Fast fallback to OpenStreetMap Nominatim API with 1.5s timeout
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=14&addressdetails=1"
                headers = {"User-Agent": "UrbanHeatAI/2.0 (contact@urbanheat.ai)"}
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    addr = data.get("address", {})
                    city = addr.get("city") or addr.get("town") or addr.get("municipality") or addr.get("suburb") or "Urban Sector"
                    state = addr.get("state") or addr.get("county") or ""
                    country = addr.get("country") or "Global"
                    name = addr.get("suburb") or addr.get("neighbourhood") or city
                    
                    return {
                        "formatted_address": data.get("display_name", f"{lat:.4f}, {lng:.4f}"),
                        "name": name,
                        "city": city,
                        "state": state,
                        "country": country,
                        "place_id": str(data.get("place_id", f"osm_{lat}_{lng}")),
                        "source": "OpenStreetMap Nominatim",
                        "status": "LIVE"
                    }
        except Exception as e:
            print(f"Nominatim Geocoding error: {e}")

        # 4. Instant Geometric fallback
        return {
            "formatted_address": f"Location at Latitude {lat:.4f}, Longitude {lng:.4f}",
            "name": f"Global Sector ({lat:.3f}, {lng:.3f})",
            "city": "Urban Coordinate Grid",
            "state": "Regional Domain",
            "country": "International",
            "place_id": f"coord_{lat:.4f}_{lng:.4f}",
            "source": "Coordinate Boundary Model",
            "status": "ESTIMATE"
        }

    async def forward_search(self, query: str) -> list:
        """
        Searches places/addresses globally.
        """
        results = []
        if not query.strip():
            return results

        # 1. Match local seeded wards
        q_lower = query.lower()
        for loc in CITIES_DATA:
            if q_lower in loc["name"].lower() or q_lower in loc["city"].lower() or q_lower in loc["state"].lower():
                results.append({
                    "name": f"{loc['name']}, {loc['city']}",
                    "latitude": loc["latitude"],
                    "longitude": loc["longitude"],
                    "formatted_address": f"{loc['name']}, {loc['city']}, {loc['state']}, India",
                    "type": "municipal_ward",
                    "source": "Municipal GIS Geodatabase"
                })

        # 2. Try Google Places / Geocoding if available
        if self.google_api_key:
            try:
                async with httpx.AsyncClient(timeout=1.5) as client:
                    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={httpx.URL(query)}&key={self.google_api_key}"
                    res = await client.get(url)
                    if res.status_code == 200 and res.json().get("status") == "OK":
                        for r in res.json().get("results", [])[:5]:
                            loc = r.get("geometry", {}).get("location", {})
                            results.append({
                                "name": r.get("formatted_address", query),
                                "latitude": loc.get("lat"),
                                "longitude": loc.get("lng"),
                                "formatted_address": r.get("formatted_address", ""),
                                "type": "place",
                                "source": "Google Places / Geocoding"
                            })
                        if results:
                            return results
            except Exception as e:
                print(f"Google Search error: {e}")

        # 3. Fallback to OSM Nominatim Search
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5&addressdetails=1"
                headers = {"User-Agent": "UrbanHeatAI/2.0 (contact@urbanheat.ai)"}
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    for r in res.json():
                        results.append({
                            "name": r.get("display_name", query),
                            "latitude": float(r.get("lat")),
                            "longitude": float(r.get("lon")),
                            "formatted_address": r.get("display_name", ""),
                            "type": r.get("type", "location"),
                            "source": "OpenStreetMap Nominatim"
                        })
        except Exception as e:
            print(f"OSM Search error: {e}")

        return results

geocoding_service = GeocodingService()
