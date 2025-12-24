"""
Etymython Image Test API Routes
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
from pydantic import BaseModel
import asyncio
import os

from .prompts import PROMPTS, get_all_prompt_ids, get_categories
from .generator import generate_and_store_image, list_test_images

router = APIRouter(prefix="/api/v1/image-test", tags=["Image Test"])

class GenerationResult(BaseModel):
    prompt_id: str
    success: bool
    full_url: Optional[str] = None
    thumb_url: Optional[str] = None
    error: Optional[str] = None

class PromptInfo(BaseModel):
    category: str
    style: str
    prompt: str

@router.get("/prompts")
async def get_prompts() -> dict[str, PromptInfo]:
    """Get all available prompts for testing."""
    return {
        k: PromptInfo(
            category=v["category"],
            style=v["style"],
            prompt=v["prompt"]
        )
        for k, v in PROMPTS.items()
    }

@router.get("/prompts/{prompt_id}")
async def get_prompt(prompt_id: str) -> PromptInfo:
    """Get a specific prompt by ID."""
    if prompt_id not in PROMPTS:
        raise HTTPException(status_code=404, detail=f"Prompt not found: {prompt_id}")
    
    p = PROMPTS[prompt_id]
    return PromptInfo(category=p["category"], style=p["style"], prompt=p["prompt"])

@router.get("/categories")
async def get_all_categories() -> list[str]:
    """Get all prompt categories."""
    return get_categories()

@router.get("/test-config")
async def test_config() -> dict:
    """Test if OpenAI API key is accessible."""
    has_env_key = bool(os.environ.get("OPENAI_API_KEY"))
    
    can_access_secret = False
    secret_error = None
    try:
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        name = "projects/etymython-project/secrets/openai-api-key/versions/latest"
        response = client.access_secret_version(request={"name": name})
        api_key = response.payload.data.decode("UTF-8")
        can_access_secret = bool(api_key and len(api_key) > 10)
    except Exception as e:
        secret_error = str(e)
    
    return {
        "has_env_variable": has_env_key,
        "can_access_secret_manager": can_access_secret,
        "secret_manager_error": secret_error
    }

@router.get("/images")
async def get_images() -> list[dict]:
    """Get all generated test images from GCS."""
    try:
        return list_test_images()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/{prompt_id}")
async def generate_image(prompt_id: str) -> GenerationResult:
    """Generate a single image for the specified prompt."""
    if prompt_id not in PROMPTS:
        raise HTTPException(status_code=404, detail=f"Prompt not found: {prompt_id}")
    
    try:
        result = await generate_and_store_image(prompt_id)
        
        if result.get("success"):
            return GenerationResult(
                prompt_id=prompt_id,
                success=True,
                full_url=result.get("full_url"),
                thumb_url=result.get("thumb_url")
            )
        else:
            return GenerationResult(
                prompt_id=prompt_id,
                success=False,
                error=result.get("error")
            )
    except Exception as e:
        return GenerationResult(
            prompt_id=prompt_id,
            success=False,
            error=str(e)
        )

@router.post("/generate-category/{category}")
async def generate_category(category: str, background_tasks: BackgroundTasks) -> dict:
    """Queue generation of all images in a category (runs in background)."""
    prompt_ids = [k for k, v in PROMPTS.items() if v["category"] == category]
    
    if not prompt_ids:
        raise HTTPException(status_code=404, detail=f"No prompts found for category: {category}")
    
    # This would run in background - for now just return the count
    return {
        "message": f"Queued {len(prompt_ids)} images for generation",
        "prompt_ids": prompt_ids,
        "estimated_cost": f"${len(prompt_ids) * 0.04:.2f}"
    }

@router.get("/stats")
async def get_stats() -> dict:
    """Get statistics about prompts and generated images."""
    images = list_test_images()
    generated_ids = {img["prompt_id"] for img in images}
    
    return {
        "total_prompts": len(PROMPTS),
        "images_generated": len(images),
        "images_pending": len(PROMPTS) - len(images),
        "categories": {
            cat: {
                "total": len([k for k, v in PROMPTS.items() if v["category"] == cat]),
                "generated": len([img for img in images if img["category"] == cat])
            }
            for cat in get_categories()
        },
        "estimated_cost_remaining": f"${(len(PROMPTS) - len(images)) * 0.04:.2f}"
    }
