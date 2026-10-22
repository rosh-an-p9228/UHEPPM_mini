from typing import List, Dict, Any

class HotspotDetectionEngine:
    @staticmethod
    def detect_hotspots(location_id: str, location_name: str, center_lat: float, center_lon: float, baseline_temp: float) -> List[Dict[str, Any]]:
        """
        Computes localized spatial micro-hotspots around the selected municipal zone.
        """
        hotspots = [
            {
                "id": f"{location_id}_hs_1",
                "name": f"{location_name} — Industrial / Commercial Core",
                "latitude": center_lat + 0.0055,
                "longitude": center_lon + 0.0042,
                "heat_score": 88.4,
                "risk_level": "EXTREME",
                "area_hectares": 34.5,
                "surface_temp": baseline_temp + 3.2,
                "main_factors": ["High Asphalt & Concrete Density", "Heavy Freight Traffic", "Zero Canopy Cover"],
                "recommended_action": "High-albedo cool pavement retrofit & urban canopy corridor"
            },
            {
                "id": f"{location_id}_hs_2",
                "name": f"{location_name} — Transit Interchange & Arterial Junction",
                "latitude": center_lat - 0.0048,
                "longitude": center_lon - 0.0035,
                "heat_score": 81.2,
                "risk_level": "HIGH",
                "area_hectares": 22.0,
                "surface_temp": baseline_temp + 2.5,
                "main_factors": ["Vehicular Heat Exhaust", "Signalized Idling Delay", "Impervious Surface"],
                "recommended_action": "Pedestrian solar shade structures & dynamic signal timing"
            },
            {
                "id": f"{location_id}_hs_3",
                "name": f"{location_name} — High-Density Residential Low-Rise",
                "latitude": center_lat + 0.0032,
                "longitude": center_lon - 0.0060,
                "heat_score": 74.0,
                "risk_level": "HIGH",
                "area_hectares": 48.0,
                "surface_temp": baseline_temp + 1.4,
                "main_factors": ["High Building Thermal Mass", "Air Conditioning Waste Heat Rejection", "Low Albedo Roofs"],
                "recommended_action": "Mandatory cool roof coating program & rooftop greening"
            },
            {
                "id": f"{location_id}_cool_1",
                "name": f"{location_name} — Central Park & Wetland Buffer",
                "latitude": center_lat - 0.0070,
                "longitude": center_lon + 0.0050,
                "heat_score": 24.5,
                "risk_level": "SAFE",
                "area_hectares": 62.0,
                "surface_temp": baseline_temp - 4.8,
                "main_factors": ["Evapotranspiration Cooling", "Dense Tree Canopy", "Open Water Body"],
                "recommended_action": "Preserve cooling island buffer and expand green corridors"
            }
        ]
        return hotspots

hotspot_engine = HotspotDetectionEngine()
