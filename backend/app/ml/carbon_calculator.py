from typing import Dict, Any

class CarbonCalculator:
    @staticmethod
    def calculate_co2_reduction(
        tree_count: int = 500,
        traffic_reduction_pct: float = 20.0,
        cool_roof_area_sq_m: float = 25000.0,
        solar_capacity_kw: float = 500.0,
        green_roof_area_sq_m: float = 10000.0
    ) -> Dict[str, Any]:
        """
        Estimates annual carbon sequestration and avoidance using IPCC / EPA emission factors.
        """
        # 1. Trees: ~21.77 kg CO2 / mature urban tree / year
        trees_offset = (tree_count * 21.77) / 1000.0 # tonnes
        
        # 2. Traffic congestion reduction: ~1.8 tonnes CO2 avoided per 1% reduction in arterial congestion per ward corridor
        traffic_offset = traffic_reduction_pct * 2.2
        
        # 3. Cool roofs: ~12.5 kg CO2 / m² / yr avoided via reduced HVAC thermal cooling load
        cool_roof_offset = (cool_roof_area_sq_m * 12.5) / 1000.0
        
        # 4. Solar rooftop energy: ~0.82 kg CO2 / kWh generated (~1400 kWh/kWp/yr)
        solar_offset = (solar_capacity_kw * 1400.0 * 0.82) / 1000.0
        
        # 5. Green roofs: ~8.2 kg CO2 / m² / yr (insulation + direct sequestration)
        green_roof_offset = (green_roof_area_sq_m * 8.2) / 1000.0
        
        total_co2 = round(trees_offset + traffic_offset + cool_roof_offset + solar_offset + green_roof_offset, 2)
        equivalent_cars = int(total_co2 / 4.6) # EPA average: 4.6 metric tons CO2 / typical passenger vehicle / year
        
        return {
            "annual_co2_reduction_tonnes": total_co2,
            "trees_offset_tco2": round(trees_offset, 2),
            "traffic_offset_tco2": round(traffic_offset, 2),
            "cool_roof_cooling_offset_tco2": round(cool_roof_offset, 2),
            "solar_clean_energy_offset_tco2": round(solar_offset, 2),
            "green_roof_offset_tco2": round(green_roof_offset, 2),
            "equivalent_cars_removed": equivalent_cars,
            "assumptions_note": "Calculations based on IPCC Urban Climate Guidelines and EPA Greenhouse Gas Equivalencies (Grid emission factor 0.82 kg CO2/kWh)."
        }

carbon_calculator = CarbonCalculator()
