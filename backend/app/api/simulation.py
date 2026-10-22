from fastapi import APIRouter
from ..schemas.schemas import SimulationRequest, SimulationResponse
from ..seed_data.seed_cities import resolve_location
from ..ml.simulator_engine import simulator_engine

router = APIRouter(prefix="/api/simulation", tags=["Urban Simulator"])

@router.post("/", response_model=SimulationResponse)
async def run_simulation(req: SimulationRequest):
    loc = resolve_location(req.location_id)
    
    result = simulator_engine.simulate_scenario(
        location_id=loc["id"],
        location_name=loc["name"],
        tree_cover_delta_pct=req.tree_cover_delta_pct,
        cool_roofs_pct=req.cool_roofs_pct,
        traffic_reduction_pct=req.traffic_reduction_pct,
        green_roofs_pct=req.green_roofs_pct,
        solar_shading_pct=req.solar_shading_pct,
        water_features_pct=req.water_features_pct
    )
    return result
