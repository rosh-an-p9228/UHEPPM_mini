from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from ..ml.image_segmenter import image_analyzer

router = APIRouter(prefix="/api/image-analysis", tags=["Image Analysis"])

@router.post("/")
async def analyze_urban_image(file: UploadFile = File(...)):
    # Validate content type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be a valid image (JPEG, PNG, WebP)")
        
    contents = await file.read()
    if len(contents) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 15MB limit")
        
    analysis = image_analyzer.analyze_image_bytes(contents, file.filename)
    return analysis

@router.get("/sample")
async def get_sample_analysis():
    """Provides a sample pre-computed image analysis for instant dashboard demonstration"""
    sample_bytes = b""
    return image_analyzer.analyze_image_bytes(sample_bytes, "urban_street_sample_nerul.jpg")
