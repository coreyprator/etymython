"""
Etymython Figure Image Generation - Production Generator
Generates Renaissance portrait images for mythological figures using DALL-E 3.
"""
import os
import asyncio
import httpx
from datetime import datetime
from typing import Optional, Dict
from google.cloud import storage
from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from PIL import Image
import io

from .figure_prompts import FIGURE_PROMPTS, get_all_figure_names

# GCS bucket configuration
BUCKET_NAME = "etymython-media"
FIGURE_FOLDER = "figure-images"

# Generation tracking (in-memory for now; could move to database)
generation_status = {
    "total": 0,
    "completed": 0,
    "failed": 0,
    "current": None,
    "errors": []
}

def get_openai_client():
    """Get AsyncOpenAI client with API key from environment or Secret Manager."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            name = "projects/etymython-project/secrets/openai-api-key/versions/latest"
            response = client.access_secret_version(request={"name": name})
            api_key = response.payload.data.decode("UTF-8").strip()
        except Exception as e:
            raise ValueError(f"Could not get OpenAI API key: {e}")
    
    if not api_key:
        raise ValueError("OpenAI API key is empty")
    
    return AsyncOpenAI(api_key=api_key, timeout=60.0)

def get_gcs_client():
    """Get GCS client."""
    return storage.Client()

async def generate_figure_image(figure_name: str) -> Dict:
    """
    Generate a single figure image using DALL-E 3.
    Returns dict with success status and image URL.
    """
    if figure_name not in FIGURE_PROMPTS:
        return {
            "figure_name": figure_name,
            "success": False,
            "error": f"No prompt found for figure: {figure_name}"
        }
    
    client = get_openai_client()
    prompt_text = FIGURE_PROMPTS[figure_name]["prompt"]
    
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        
        return {
            "figure_name": figure_name,
            "success": True,
            "image_url": image_url,
            "revised_prompt": revised_prompt,
            "error": None
        }
    except Exception as e:
        return {
            "figure_name": figure_name,
            "success": False,
            "image_url": None,
            "revised_prompt": None,
            "error": str(e)
        }

async def download_and_create_thumbnails(image_url: str, figure_name: str) -> Dict:
    """
    Download image from DALL-E and create both full and thumbnail versions.
    Upload to GCS and return public URLs.
    """
    gcs_client = get_gcs_client()
    bucket = gcs_client.bucket(BUCKET_NAME)
    
    # Use figure name as filename (normalized)
    filename = figure_name.lower().replace(" ", "_") + ".png"
    
    # Download original image
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(image_url)
        image_data = response.content
    
    # Upload full-size image (1024x1024)
    full_path = f"{FIGURE_FOLDER}/full/{filename}"
    blob = bucket.blob(full_path)
    blob.upload_from_string(image_data, content_type="image/png")
    blob.make_public()
    
    # Create thumbnail (80x80)
    img = Image.open(io.BytesIO(image_data))
    
    # Center crop to square (already square from DALL-E but being safe)
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img_cropped = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Resize to 80x80 thumbnail
    img_thumb = img_cropped.resize((80, 80), Image.Resampling.LANCZOS)
    
    # Save thumbnail
    thumb_buffer = io.BytesIO()
    img_thumb.save(thumb_buffer, format="PNG")
    thumb_data = thumb_buffer.getvalue()
    
    thumb_path = f"{FIGURE_FOLDER}/thumbs/{filename}"
    thumb_blob = bucket.blob(thumb_path)
    thumb_blob.upload_from_string(thumb_data, content_type="image/png")
    thumb_blob.make_public()
    
    return {
        "full_url": blob.public_url,
        "thumb_url": thumb_blob.public_url,
        "full_path": full_path,
        "thumb_path": thumb_path
    }

async def generate_and_store_figure(figure_name: str, db: Session = None) -> Dict:
    """
    Complete pipeline: generate image, download, create thumbnails, upload to GCS.
    Optionally update database with image URLs.
    """
    try:
        # Update status
        generation_status["current"] = figure_name
        
        # Generate with DALL-E
        result = await generate_figure_image(figure_name)
        
        if not result["success"]:
            generation_status["failed"] += 1
            generation_status["errors"].append({
                "figure": figure_name,
                "error": result["error"]
            })
            return result
        
        # Download and upload to GCS
        gcs_result = await download_and_create_thumbnails(result["image_url"], figure_name)
        
        # Update database if session provided
        if db:
            from app import models
            figure = db.query(models.MythologicalFigure).filter(
                models.MythologicalFigure.english_name == figure_name
            ).first()
            
            if figure:
                figure.image_url = gcs_result["thumb_url"]  # Use thumbnail for family tree
                db.commit()
        
        generation_status["completed"] += 1
        
        return {
            "figure_name": figure_name,
            "figure_type": FIGURE_PROMPTS[figure_name]["figure_type"],
            "success": True,
            "full_url": gcs_result["full_url"],
            "thumb_url": gcs_result["thumb_url"],
            "dalle_url": result["image_url"],
            "revised_prompt": result["revised_prompt"],
            "error": None
        }
    except Exception as e:
        generation_status["failed"] += 1
        generation_status["errors"].append({
            "figure": figure_name,
            "error": str(e)
        })
        return {
            "figure_name": figure_name,
            "success": False,
            "error": f"Pipeline failed: {type(e).__name__}: {str(e)}"
        }

async def generate_all_figures(db: Session = None, delay_seconds: float = 2.0) -> list[Dict]:
    """
    Generate images for all figures with delay between requests.
    Returns list of results for each figure.
    """
    figure_names = get_all_figure_names()
    
    # Initialize status
    generation_status["total"] = len(figure_names)
    generation_status["completed"] = 0
    generation_status["failed"] = 0
    generation_status["current"] = None
    generation_status["errors"] = []
    
    results = []
    for i, figure_name in enumerate(figure_names):
        print(f"Generating {i+1}/{len(figure_names)}: {figure_name}")
        result = await generate_and_store_figure(figure_name, db)
        results.append(result)
        
        # Delay between requests to avoid rate limits
        if i < len(figure_names) - 1:
            await asyncio.sleep(delay_seconds)
    
    generation_status["current"] = None
    return results

def list_generated_figures() -> list[Dict]:
    """List all generated figure images from GCS."""
    gcs_client = get_gcs_client()
    bucket = gcs_client.bucket(BUCKET_NAME)
    
    images = []
    blobs = bucket.list_blobs(prefix=f"{FIGURE_FOLDER}/full/")
    
    for blob in blobs:
        if not blob.name.endswith('.png'):
            continue
            
        filename = blob.name.split("/")[-1]
        figure_name = filename.replace(".png", "").replace("_", " ").title()
        
        thumb_path = f"{FIGURE_FOLDER}/thumbs/{filename}"
        
        # Check if we have prompt data for this figure
        prompt_data = FIGURE_PROMPTS.get(figure_name, {})
        
        images.append({
            "figure_name": figure_name,
            "figure_type": prompt_data.get("figure_type", "Unknown"),
            "full_url": blob.public_url,
            "thumb_url": f"https://storage.googleapis.com/{BUCKET_NAME}/{thumb_path}",
            "created_at": blob.time_created.isoformat() if blob.time_created else None
        })
    
    return images

def get_generation_status() -> Dict:
    """Get current generation status."""
    return {
        "total": generation_status["total"],
        "completed": generation_status["completed"],
        "failed": generation_status["failed"],
        "current": generation_status["current"],
        "in_progress": generation_status["current"] is not None,
        "progress_percent": round((generation_status["completed"] / generation_status["total"] * 100), 1) if generation_status["total"] > 0 else 0,
        "errors": generation_status["errors"]
    }

def reset_generation_status():
    """Reset generation status tracking."""
    generation_status["total"] = 0
    generation_status["completed"] = 0
    generation_status["failed"] = 0
    generation_status["current"] = None
    generation_status["errors"] = []
