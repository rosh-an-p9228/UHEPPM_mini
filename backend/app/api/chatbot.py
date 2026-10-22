import os
from fastapi import APIRouter
from pydantic import BaseModel
from ..config import settings
from ..schemas.schemas import ChatRequest, ChatResponse
from ..services.ai_assistant_service import ai_assistant_service

router = APIRouter(prefix="/chat", tags=["AI Assistant"])

class SetKeyRequest(BaseModel):
    api_key: str
    model: str = "gpt-4o-mini"

@router.get("/status")
async def get_chat_status():
    key = (settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")).strip()
    return {
        "provider": "OpenAI ChatGPT",
        "model": settings.OPENAI_MODEL or "gpt-4o-mini",
        "is_configured": bool(key),
        "key_preview": f"{key[:6]}...{key[-4:]}" if len(key) > 10 else ("Configured" if key else "Not Configured"),
        "realtime_telemetry_grounding": True,
        "features": [
            "Open-Meteo Real-Time Weather Integration",
            "NASA MODIS / USGS Landsat 9 Radiative Skin LST Fusion",
            "Copernicus Sentinel-2 MSI 10m Canopy Index Grounding",
            "OpenAQ / CPCB Particulate Pollution Context",
            "TomTom Arterial Traffic Delay Grounding",
            "Multi-Turn Conversation Memory"
        ]
    }

@router.post("/set-key")
async def set_openai_key(req: SetKeyRequest):
    new_key = req.api_key.strip()
    new_model = req.model.strip() or "gpt-4o-mini"
    settings.OPENAI_API_KEY = new_key
    settings.OPENAI_MODEL = new_model
    os.environ["OPENAI_API_KEY"] = new_key
    os.environ["OPENAI_MODEL"] = new_model
    
    # Also persist to local .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = [line for line in f.readlines() if not line.startswith("OPENAI_API_KEY=") and not line.startswith("OPENAI_MODEL=")]
    lines.append(f"OPENAI_API_KEY={new_key}\n")
    lines.append(f"OPENAI_MODEL={new_model}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    return {
        "success": True,
        "message": "OpenAI API Key successfully configured and persisted.",
        "model": new_model,
        "is_configured": True
    }

@router.post("/", response_model=ChatResponse)
async def chat_with_climate_ai(req: ChatRequest):
    return await ai_assistant_service.generate_response(
        message=req.message,
        location_id=req.location_id,
        lat=req.lat,
        lng=req.lng,
        telemetry=req.telemetry,
        chat_history=req.chat_history
    )

