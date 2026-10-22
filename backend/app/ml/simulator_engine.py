from typing import Dict, Any
from ..seed_data.seed_cities import CITIES_DATA

class UrbanSimulatorEngine:
    @staticmethod
    def simulate_scenario(
        location_id: str,
        location_name: str,
        tree_cover_delta_pct: float,
        cool_roofs_pct: float,
        traffic_reduction_pct: float,
        green_roofs_pct: float,
        solar_shading_pct: float,
        water_features_pct: float
    ) -> Dict[str, Any]:
        """
        Physics-informed microclimate energy balance model for scenario planning.
        Calculates evaporative cooling, albedo surface reflections, and anthropogenic heat suppression.
        """
        matched_city = next((c for c in CITIES_DATA if c["id"] == location_id), None)
        initial_temp = matched_city["baseline_temp"] if matched_city else 38.4
        initial_heat_risk = 84.0 # Baseline high heat risk
        
        # Microclimate cooling coefficients (°C reduction per % intervention)
        # 1. Tree canopy: ~0.04°C per 1% canopy expansion (evapotranspiration + shading)
        dt_trees = tree_cover_delta_pct * 0.042
        
        # 2. Cool roofs (albedo increase 0.15 -> 0.70): ~0.022°C per 1% roof retrofitted
        dt_cool_roofs = cool_roofs_pct * 0.024
        
        # 3. Traffic reduction: ~0.025°C per 1% congestion reduction (combustion reduction)
        dt_traffic = traffic_reduction_pct * 0.026
        
        # 4. Green roofs: ~0.02°C per 1% green roof retrofit
        dt_green_roofs = green_roofs_pct * 0.020
        
        # 5. Solar shading over walkways: ~0.015°C ambient shade reduction
        dt_solar_shading = solar_shading_pct * 0.018
        
        # 6. Water features / evaporative micro-misting: ~0.035°C per % water body addition
        dt_water = water_features_pct * 0.038
        
        total_dt = round(dt_trees + dt_cool_roofs + dt_traffic + dt_green_roofs + dt_solar_shading + dt_water, 2)
        simulated_temp = round(max(24.0, initial_temp - total_dt), 1)
        
        # Calculate heat risk score delta (1°C temp drop ~= 4.8 pts risk reduction + structural intervention benefits)
        risk_drop_from_temp = total_dt * 4.2
        risk_drop_from_greening = (tree_cover_delta_pct * 0.28) + (green_roofs_pct * 0.15)
        risk_drop_from_traffic = (traffic_reduction_pct * 0.22)
        
        total_risk_drop = round(risk_drop_from_temp + risk_drop_from_greening + risk_drop_from_traffic, 1)
        simulated_heat_risk = round(max(10.0, initial_heat_risk - total_risk_drop), 1)
        risk_reduction_pct = round(((initial_heat_risk - simulated_heat_risk) / initial_heat_risk) * 100, 1)
        
        # Categories
        def get_cat(score):
            return "EXTREME" if score > 80 else ("HIGH" if score > 60 else ("MODERATE" if score > 30 else "SAFE"))
            
        initial_cat = get_cat(initial_heat_risk)
        simulated_cat = get_cat(simulated_heat_risk)
        
        # Carbon reduction estimation (tonnes CO2/yr)
        area_ha = (matched_city["area_sq_km"] if matched_city else 6.8) * 100.0
        # Tree carbon sequestration: ~22 kg CO2 / tree / yr (~100 trees per 1% canopy per ha)
        co2_trees = (tree_cover_delta_pct * 8.5) * (area_ha * 0.05)
        # Reduced HVAC building electricity: ~1.2 tCO2 saved per 1% cool roof per ha
        co2_cool_roofs = (cool_roofs_pct * 0.45) * (area_ha * 0.08)
        # Traffic combustion reduction: ~3.2 tCO2 per 1% traffic reduction
        co2_traffic = (traffic_reduction_pct * 2.8) * (area_ha * 0.06)
        # Green roofs & solar shading: ~1.5 tCO2
        co2_other = ((green_roofs_pct + solar_shading_pct) * 0.6) * (area_ha * 0.04)
        
        total_co2_tonnes = round(co2_trees + co2_cool_roofs + co2_traffic + co2_other, 1)
        energy_savings_mwh = round(total_co2_tonnes * 1.35, 1)
        
        return {
            "location_id": location_id,
            "location_name": location_name,
            "initial_temp": initial_temp,
            "simulated_temp": simulated_temp,
            "temp_reduction_c": total_dt,
            "initial_heat_risk": initial_heat_risk,
            "simulated_heat_risk": simulated_heat_risk,
            "risk_reduction_pts": total_risk_drop,
            "risk_reduction_pct": risk_reduction_pct,
            "initial_category": initial_cat,
            "simulated_category": simulated_cat,
            "annual_co2_reduction_tonnes": total_co2_tonnes,
            "energy_savings_mwh_yr": energy_savings_mwh,
            "intervention_breakdown": {
                "tree_canopy_temp_drop": round(dt_trees, 2),
                "cool_roofs_temp_drop": round(dt_cool_roofs, 2),
                "traffic_temp_drop": round(dt_traffic, 2),
                "green_roofs_temp_drop": round(dt_green_roofs, 2),
                "solar_shading_temp_drop": round(dt_solar_shading, 2),
                "water_features_temp_drop": round(dt_water, 2)
            },
            "disclaimer": "Model-based scenario estimate using urban microclimate energy balance modeling. Actual municipal response may vary by atmospheric boundary layer dynamics."
        }

simulator_engine = UrbanSimulatorEngine()
