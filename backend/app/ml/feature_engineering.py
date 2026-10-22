from datetime import datetime, timezone
from typing import Dict, Any, List
import numpy as np

class FeatureEngineering:
    @staticmethod
    def extract_features(
        temp: float,
        humidity: float,
        wind_speed: float,
        uv_index: float,
        lst: float,
        ndvi: float,
        congestion_index: float,
        traffic_heat: float,
        aqi: float,
        pop_density: float,
        building_density: float = 0.65,
        target_hour_offset: int = 1
    ) -> Dict[str, float]:
        """
        Builds engineered feature vector for urban heat prediction models.
        """
        now = datetime.now(timezone.utc)
        target_hour = (now.hour + target_hour_offset) % 24
        
        # Diurnal solar cycle
        solar_angle = np.sin(np.pi * (target_hour - 6) / 12) if 6 <= target_hour <= 18 else -0.3
        
        # Heat Index (Rothfusz approximation for air temp + humidity interaction)
        hi_interaction = temp + 0.5555 * ((humidity / 100.0) * 6.11 * np.exp(5417.7530 * (1/273.16 - 1/(273.15 + temp))) - 10.0)
        
        # Inverse vegetation heat trap
        vegetation_cooling_deficit = max(0.0, 1.0 - ndvi)
        
        # Surface-atmosphere thermal gradient
        thermal_gradient = max(0.0, lst - temp)
        
        # Urban canopy friction (wind reduction from buildings)
        effective_wind_cooling = max(0.2, wind_speed * (1.0 - building_density * 0.7))
        
        return {
            "current_temp": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "uv_index": uv_index,
            "lst": lst,
            "ndvi": ndvi,
            "congestion_index": congestion_index,
            "traffic_heat": traffic_heat,
            "aqi": aqi,
            "pop_density": pop_density,
            "building_density": building_density,
            "solar_angle": float(solar_angle),
            "hi_interaction": float(hi_interaction),
            "vegetation_cooling_deficit": float(vegetation_cooling_deficit),
            "thermal_gradient": float(thermal_gradient),
            "effective_wind_cooling": float(effective_wind_cooling),
            "target_hour": target_hour
        }

feature_engineer = FeatureEngineering()
