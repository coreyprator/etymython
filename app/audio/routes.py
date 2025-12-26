"""Audio generation API routes."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app import models
from app.audio.generator import generate_pronunciation_audio

router = APIRouter(prefix="/api/v1/audio", tags=["audio"])


class AudioGenerationResponse(BaseModel):
    figure_id: int
    figure_name: str
    audio_url: str
    message: str


class BatchAudioResponse(BaseModel):
    total: int
    successful: int
    failed: int
    details: List[dict]


@router.post("/generate/{figure_id}", response_model=AudioGenerationResponse)
async def generate_audio_for_figure(
    figure_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate pronunciation audio for a specific figure.
    """
    # Get figure
    figure = db.query(models.MythologicalFigure).filter(
        models.MythologicalFigure.id == figure_id
    ).first()
    
    if not figure:
        raise HTTPException(status_code=404, detail="Figure not found")
    
    if not figure.greek_name:
        raise HTTPException(
            status_code=400, 
            detail=f"Figure {figure.english_name} has no Greek name"
        )
    
    try:
        # Generate audio
        audio_url = await generate_pronunciation_audio(
            greek_name=figure.greek_name,
            english_name=figure.english_name
        )
        
        # Update database
        figure.pronunciation_audio_url = audio_url
        db.commit()
        
        return AudioGenerationResponse(
            figure_id=figure.id,
            figure_name=figure.english_name,
            audio_url=audio_url,
            message="Audio generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Audio generation failed: {str(e)}"
        )


@router.post("/generate-all", response_model=BatchAudioResponse)
async def generate_audio_for_all_figures(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate pronunciation audio for all figures with Greek names.
    Runs as background task to avoid timeout.
    """
    # Get all figures with Greek names
    figures = db.query(models.MythologicalFigure).filter(
        models.MythologicalFigure.greek_name.isnot(None),
        models.MythologicalFigure.greek_name != ""
    ).all()
    
    results = {
        "total": len(figures),
        "successful": 0,
        "failed": 0,
        "details": []
    }
    
    for figure in figures:
        try:
            # Generate audio
            audio_url = await generate_pronunciation_audio(
                greek_name=figure.greek_name,
                english_name=figure.english_name
            )
            
            # Update database
            figure.pronunciation_audio_url = audio_url
            db.commit()
            
            results["successful"] += 1
            results["details"].append({
                "figure_id": figure.id,
                "figure_name": figure.english_name,
                "status": "success",
                "audio_url": audio_url
            })
            
        except Exception as e:
            results["failed"] += 1
            results["details"].append({
                "figure_id": figure.id,
                "figure_name": figure.english_name,
                "status": "failed",
                "error": str(e)
            })
    
    return BatchAudioResponse(**results)


@router.get("/status")
async def get_audio_status(db: Session = Depends(get_db)):
    """
    Get audio generation status - how many figures have audio.
    """
    total = db.query(models.MythologicalFigure).count()
    with_audio = db.query(models.MythologicalFigure).filter(
        models.MythologicalFigure.pronunciation_audio_url.isnot(None)
    ).count()
    
    return {
        "total_figures": total,
        "with_audio": with_audio,
        "without_audio": total - with_audio,
        "percentage": round((with_audio / total * 100) if total > 0 else 0, 1)
    }
