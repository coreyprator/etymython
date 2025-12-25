"""
Etymython Figure Image Generation - API Routes
Endpoints for generating and retrieving figure images.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import asyncio

from app.database import get_db
from .generator import (
    generate_and_store_figure,
    generate_all_figures,
    list_generated_figures,
    get_generation_status,
    reset_generation_status
)
from .figure_prompts import get_all_figure_names, get_figure_types

router = APIRouter(prefix="/api/v1/images", tags=["Figure Images"])

class GenerationResult(BaseModel):
    figure_name: str
    success: bool
    full_url: Optional[str] = None
    thumb_url: Optional[str] = None
    error: Optional[str] = None

class GenerationStatus(BaseModel):
    total: int
    completed: int
    failed: int
    current: Optional[str]
    in_progress: bool
    progress_percent: float
    errors: List[dict]

class FigureImage(BaseModel):
    figure_name: str
    figure_type: str
    full_url: str
    thumb_url: str
    created_at: Optional[str]

@router.get("/available-figures")
async def get_available_figures() -> dict:
    """Get list of all figures that have prompts available."""
    return {
        "figures": get_all_figure_names(),
        "figure_types": get_figure_types(),
        "total": len(get_all_figure_names())
    }

@router.get("/generated")
async def get_generated_images() -> List[FigureImage]:
    """Get list of all generated figure images from GCS."""
    try:
        images = list_generated_figures()
        return [FigureImage(**img) for img in images]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/for-frontend")
async def get_images_for_frontend() -> dict:
    """
    Get images formatted for frontend Cytoscape integration.
    Returns a mapping of figure names to thumbnail URLs.
    """
    try:
        images = list_generated_figures()
        return {
            img["figure_name"]: img["thumb_url"] 
            for img in images
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/{figure_name}")
async def generate_single_figure(
    figure_name: str,
    db: Session = Depends(get_db)
) -> GenerationResult:
    """Generate image for a single figure."""
    if figure_name not in get_all_figure_names():
        raise HTTPException(
            status_code=404,
            detail=f"Figure not found: {figure_name}"
        )
    
    try:
        result = await generate_and_store_figure(figure_name, db)
        
        return GenerationResult(
            figure_name=result["figure_name"],
            success=result["success"],
            full_url=result.get("full_url"),
            thumb_url=result.get("thumb_url"),
            error=result.get("error")
        )
    except Exception as e:
        return GenerationResult(
            figure_name=figure_name,
            success=False,
            error=str(e)
        )

async def run_batch_generation(db: Session):
    """Background task to generate all figures."""
    try:
        await generate_all_figures(db=db, delay_seconds=2.0)
    except Exception as e:
        print(f"Batch generation error: {e}")

@router.post("/generate-all")
async def start_batch_generation(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> dict:
    """
    Start batch generation of all figure images in background.
    Returns immediately with status endpoint.
    """
    status = get_generation_status()
    if status["in_progress"]:
        return {
            "message": "Generation already in progress",
            "status": status
        }
    
    # Reset status and start background task
    reset_generation_status()
    background_tasks.add_task(run_batch_generation, db)
    
    figure_count = len(get_all_figure_names())
    estimated_cost = figure_count * 0.04  # $0.04 per image
    
    return {
        "message": f"Started batch generation of {figure_count} figures",
        "estimated_cost": f"${estimated_cost:.2f}",
        "estimated_time": f"{figure_count * 3 / 60:.1f} minutes",
        "status_endpoint": "/api/v1/images/generate-status"
    }

@router.get("/generate-status")
async def check_generation_status() -> GenerationStatus:
    """Check the status of ongoing batch generation."""
    status = get_generation_status()
    return GenerationStatus(**status)

@router.post("/reset-status")
async def reset_status() -> dict:
    """Reset generation status (admin endpoint)."""
    reset_generation_status()
    return {"message": "Status reset successfully"}

@router.get("/stats")
async def get_image_stats() -> dict:
    """Get statistics about generated images."""
    images = list_generated_figures()
    
    # Group by figure type
    by_type = {}
    for img in images:
        fig_type = img["figure_type"]
        if fig_type not in by_type:
            by_type[fig_type] = 0
        by_type[fig_type] += 1
    
    total_available = len(get_all_figure_names())
    total_generated = len(images)
    
    return {
        "total_available": total_available,
        "total_generated": total_generated,
        "remaining": total_available - total_generated,
        "progress_percent": round((total_generated / total_available * 100), 1) if total_available > 0 else 0,
        "by_type": by_type,
        "estimated_cost_remaining": f"${(total_available - total_generated) * 0.04:.2f}",
        "total_cost_if_all": f"${total_available * 0.04:.2f}"
    }
