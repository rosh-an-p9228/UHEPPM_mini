from fastapi import APIRouter
from ..schemas.schemas import CarbonCalcRequest, CarbonCalcResponse
from ..ml.carbon_calculator import carbon_calculator

router = APIRouter(prefix="/api/carbon", tags=["Carbon Calculator"])

@router.post("/calculate", response_model=CarbonCalcResponse)
async def calculate_carbon_offset(req: CarbonCalcRequest):
    return carbon_calculator.calculate_co2_reduction(
        tree_count=req.tree_count,
        traffic_reduction_pct=req.traffic_reduction_pct,
        cool_roof_area_sq_m=req.cool_roof_area_sq_m,
        solar_capacity_kw=req.solar_capacity_kw,
        green_roof_area_sq_m=req.green_roof_area_sq_m
    )
