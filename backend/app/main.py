from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db

# Import all API routers
from .api.locations import router as locations_router
from .api.dashboard import router as dashboard_router
from .api.location_data import router as location_data_router
from .api.search import router as search_router
from .api.weather import router as weather_router
from .api.satellite import router as satellite_router
from .api.vegetation import router as vegetation_router
from .api.traffic import router as traffic_router
from .api.pollution import router as pollution_router
from .api.population import router as population_router
from .api.predictions import router as predictions_router
from .api.explainability import router as explainability_router
from .api.recommendations import router as recommendations_router
from .api.heatwave import router as heatwave_router
from .api.vulnerability import router as vulnerability_router
from .api.simulation import router as simulation_router
from .api.carbon import router as carbon_router
from .api.image_analysis import router as image_analysis_router
from .api.chatbot import router as chatbot_router
from .api.api_status import router as api_status_router
from .api.auth import router as auth_router

app = FastAPI(
    title="UrbanHeat AI — API Platform",
    description="Backend microservices for Urban Climate Intelligence, Satellite Earth Observation, and Scenario Prevention Planning.",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers cleanly (each router module defines its /api/... path)
app.include_router(location_data_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(locations_router)
app.include_router(dashboard_router)
app.include_router(weather_router)
app.include_router(satellite_router)
app.include_router(vegetation_router)
app.include_router(traffic_router)
app.include_router(pollution_router)
app.include_router(population_router)
app.include_router(predictions_router)
app.include_router(explainability_router)
app.include_router(recommendations_router)
app.include_router(heatwave_router)
app.include_router(vulnerability_router)
app.include_router(simulation_router)
app.include_router(carbon_router)
app.include_router(image_analysis_router)
app.include_router(chatbot_router, prefix="/api")
app.include_router(api_status_router)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {
        "app": "UrbanHeat AI",
        "tagline": "Predict. Understand. Prevent Urban Heat.",
        "status": "Operational",
        "version": "2.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
