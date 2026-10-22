from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Location Schemas
class LocationBase(BaseModel):
    id: str
    name: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    area_sq_km: float = 5.0
    baseline_population: int = 50000
    baseline_ndvi: float = 0.25

class LocationDetail(LocationBase):
    boundary_geojson: Optional[Dict[str, Any]] = None

# Weather Schemas
class WeatherReading(BaseModel):
    location_id: str
    location_name: str
    temperature: float
    feels_like: float
    humidity: float
    wind_speed: float
    wind_deg: float = 0.0
    uv_index: float = 5.0
    pressure: float = 1012.0
    rainfall: float = 0.0
    cloud_cover: float = 10.0
    condition: str = "Clear"
    source: str = "OpenWeather"
    is_demo: bool = False
    recorded_at: datetime
    data_label: str = "Latest available observation"

# Satellite LST Schemas
class SatelliteObservation(BaseModel):
    location_id: str
    location_name: str
    lst_day: float
    lst_night: float
    heat_intensity: str = "High"
    cloud_coverage: float = 5.0
    sensor: str = "MODIS Terra/Aqua & Landsat 9"
    is_demo: bool = True
    observation_date: datetime
    data_label: str = "Latest available satellite observation"

# Vegetation / NDVI Schemas
class VegetationReading(BaseModel):
    location_id: str
    location_name: str
    ndvi: float
    green_cover_pct: float
    tree_density_pct: float
    vegetation_class: str
    target_green_cover_pct: float = 30.0
    gap_pct: float = 12.0
    sensor: str = "Sentinel-2 MSI"
    is_demo: bool = True
    observation_date: datetime
    data_label: str = "Periodically updated satellite observation"

# Traffic Heat Schemas
class TrafficReading(BaseModel):
    location_id: str
    location_name: str
    congestion_index: float
    congestion_pct: float
    current_speed_kmh: float
    free_flow_speed_kmh: float
    delay_seconds: float = 0.0
    estimated_vehicle_activity: str = "High"
    traffic_heat_contribution: float
    traffic_heat_level: str = "Moderate"
    source: str = "TomTom Traffic API"
    is_demo: bool = True
    recorded_at: datetime
    data_label: str = "Estimated traffic heat contribution"

# Air Quality Schemas
class AirQualityReading(BaseModel):
    location_id: str
    location_name: str
    aqi: int
    category: str
    pm25: float
    pm10: float
    no2: float
    so2: float = 12.0
    o3: float = 45.0
    co: float = 0.8
    source: str = "OpenAQ / CPCB"
    is_demo: bool = True
    recorded_at: datetime
    data_label: str = "Near-real-time atmospheric sensor observation"

# Heat Risk Score Breakdown
class HeatRiskFactor(BaseModel):
    factor_name: str
    contribution_pts: float
    percentage: float
    description: str

class HeatRiskIndex(BaseModel):
    location_id: str
    location_name: str
    risk_score: float
    risk_category: str # SAFE, MODERATE, HIGH, EXTREME
    factors: List[HeatRiskFactor]
    summary_explanation: str
    delta_from_last_hour: float = 0.0
    data_label: str = "Model-based calibrated index (0-100)"

# AI Prediction Schemas
class PredictionItem(BaseModel):
    horizon: str # NOW, 1 HR, 3 HR, 6 HR, 24 HR, Tomorrow
    timestamp: datetime
    predicted_temp: float
    confidence_lower: float
    confidence_upper: float
    heat_risk_score: float
    risk_category: str

class AIPredictionResponse(BaseModel):
    location_id: str
    location_name: str
    current_temp: float
    model_version: str = "XGBoost-Climate v2.1"
    predictions: List[PredictionItem]
    shap_explanation: List[Dict[str, Any]]
    human_readable_summary: str
    data_label: str = "Model prediction with 95% confidence interval"

# Recommendation Schemas
class RecommendationItem(BaseModel):
    id: str
    category: str
    title: str
    reason: str
    priority: str # LOW, MEDIUM, HIGH, CRITICAL
    expected_temp_reduction_range: str
    expected_temp_reduction_min: float
    expected_temp_reduction_max: float
    expected_risk_reduction: float
    implementation_difficulty: str
    cost_category: str
    status: str = "Recommended"

# Heatwave Alert Schemas
class HeatAlertItem(BaseModel):
    id: int
    location_id: str
    location_name: str
    alert_type: str
    severity: str # Information, Warning, High, Critical
    title: str
    description: str
    max_predicted_temp: float
    expected_duration_days: int
    recommended_actions: List[str]
    valid_from: datetime
    valid_until: datetime

# Vulnerability Schemas
class VulnerabilityScore(BaseModel):
    location_id: str
    location_name: str
    exposure_score: float
    sensitivity_score: float
    adaptive_capacity_score: float
    overall_vulnerability_score: float
    vulnerability_category: str
    exposure_factors: List[str]
    sensitive_receptors: List[str]
    adaptive_resources: List[str]
    explanation: str

# Urban Planning Simulator Request & Response
class SimulationRequest(BaseModel):
    location_id: str
    tree_cover_delta_pct: float = Field(0.0, ge=0.0, le=50.0)
    cool_roofs_pct: float = Field(0.0, ge=0.0, le=100.0)
    traffic_reduction_pct: float = Field(0.0, ge=0.0, le=50.0)
    green_roofs_pct: float = Field(0.0, ge=0.0, le=50.0)
    solar_shading_pct: float = Field(0.0, ge=0.0, le=50.0)
    water_features_pct: float = Field(0.0, ge=0.0, le=30.0)

class SimulationResponse(BaseModel):
    location_id: str
    location_name: str
    initial_temp: float
    simulated_temp: float
    temp_reduction_c: float
    initial_heat_risk: float
    simulated_heat_risk: float
    risk_reduction_pts: float
    risk_reduction_pct: float
    initial_category: str
    simulated_category: str
    annual_co2_reduction_tonnes: float
    energy_savings_mwh_yr: float
    disclaimer: str = "Model-based scenario estimate using urban microclimate energy balance modeling."

# Carbon Calculator Request & Response
class CarbonCalcRequest(BaseModel):
    tree_count: int = 500
    traffic_reduction_pct: float = 20.0
    cool_roof_area_sq_m: float = 25000.0
    solar_capacity_kw: float = 500.0
    green_roof_area_sq_m: float = 10000.0

class CarbonCalcResponse(BaseModel):
    annual_co2_reduction_tonnes: float
    trees_offset_tco2: float
    traffic_offset_tco2: float
    cool_roof_cooling_offset_tco2: float
    solar_clean_energy_offset_tco2: float
    green_roof_offset_tco2: float
    equivalent_cars_removed: int
    assumptions_note: str

# Image Analysis Schemas
class ImageAnalysisResponse(BaseModel):
    filename: str
    tree_coverage_pct: float
    built_up_pct: float
    road_pct: float
    shade_pct: float
    open_space_pct: float
    vehicle_count_estimate: int
    visual_heat_exposure_score: float # 0-100
    exposure_rating: str # Low, Moderate, High, Extreme
    albedo_estimate: float
    cooling_recommendations: List[str]
    detected_features: List[Dict[str, Any]]
    disclaimer: str = "Visual heat exposure estimate based on optical surface materials. Not direct thermal measurement."

# AI Chatbot Schemas
class ChatRequest(BaseModel):
    message: str
    location_id: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    telemetry: Optional[Dict[str, Any]] = None
    chat_history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    suggested_followups: List[str]
    context_location: Optional[str] = None
    data_sources_referenced: List[str] = []

# API Status Schema
class ApiServiceStatus(BaseModel):
    service_name: str
    status: str # Operational, Delayed, Unavailable, Demo Mode
    response_time_ms: int
    last_successful_update: str
    last_error: Optional[str] = None
    endpoint_url: str
    data_transparency_note: str
