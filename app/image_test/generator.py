"""
Etymython Image Style Test - DALL-E 3 Generator
Generates images from prompts and stores in GCS.
"""
import os
import asyncio
import httpx
from datetime import datetime
from typing import Optional
from google.cloud import storage
from openai import AsyncOpenAI
from .prompts import PROMPTS, get_all_prompt_ids

# GCS bucket for images
BUCKET_NAME = "etymython-media"
TEST_FOLDER = "style-test"

def get_openai_client():
    """Get AsyncOpenAI client with API key from environment or Secret Manager."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Try to get from Secret Manager
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

async def generate_single_image(prompt_id: str, prompt_text: str) -> dict:
    """
    Generate a single image using DALL-E 3.
    Returns dict with image URL, local path info.
    """
    client = get_openai_client()
    
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",  # or "hd" for higher quality ($0.08 vs $0.04)
            n=1,
        )
        
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        
        return {
            "prompt_id": prompt_id,
            "success": True,
            "image_url": image_url,
            "revised_prompt": revised_prompt,
            "error": None
        }
    except Exception as e:
        return {
            "prompt_id": prompt_id,
            "success": False,
            "image_url": None,
            "revised_prompt": None,
            "error": str(e)
        }

async def download_and_upload_to_gcs(image_url: str, prompt_id: str) -> dict:
    """
    Download image from DALL-E URL and upload to GCS.
    Returns GCS paths for full image and thumbnail.
    """
    gcs_client = get_gcs_client()
    bucket = gcs_client.bucket(BUCKET_NAME)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prompt_id}_{timestamp}.png"
    
    # Download image
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(image_url)
        image_data = response.content
    
    # Upload full-size image
    full_path = f"{TEST_FOLDER}/full/{filename}"
    blob = bucket.blob(full_path)
    blob.upload_from_string(image_data, content_type="image/png")
    
    # Generate thumbnail (80x80) using PIL
    from PIL import Image
    import io
    
    img = Image.open(io.BytesIO(image_data))
    
    # Create square crop from center
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img_cropped = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Resize to 80x80
    img_thumb = img_cropped.resize((80, 80), Image.Resampling.LANCZOS)
    
    # Save thumbnail
    thumb_buffer = io.BytesIO()
    img_thumb.save(thumb_buffer, format="PNG")
    thumb_data = thumb_buffer.getvalue()
    
    thumb_path = f"{TEST_FOLDER}/thumbs/{filename}"
    thumb_blob = bucket.blob(thumb_path)
    thumb_blob.upload_from_string(thumb_data, content_type="image/png")
    
    # Make both publicly accessible
    blob.make_public()
    thumb_blob.make_public()
    
    return {
        "full_url": blob.public_url,
        "thumb_url": thumb_blob.public_url,
        "full_path": full_path,
        "thumb_path": thumb_path
    }

async def generate_and_store_image(prompt_id: str) -> dict:
    """
    Full pipeline: generate image, download, create thumbnail, upload to GCS.
    """
    try:
        if prompt_id not in PROMPTS:
            return {"success": False, "error": f"Unknown prompt_id: {prompt_id}"}
        
        prompt_info = PROMPTS[prompt_id]
        
        # Generate with DALL-E
        result = await generate_single_image(prompt_id, prompt_info["prompt"])
        
        if not result["success"]:
            return result
        
        # Download and upload to GCS
        gcs_result = await download_and_upload_to_gcs(result["image_url"], prompt_id)
        
        return {
            "prompt_id": prompt_id,
            "category": prompt_info["category"],
            "style": prompt_info["style"],
            "prompt": prompt_info["prompt"],
            "revised_prompt": result["revised_prompt"],
            "success": True,
            "full_url": gcs_result["full_url"],
            "thumb_url": gcs_result["thumb_url"],
            "dalle_url": result["image_url"],  # Temporary URL, expires
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Generation pipeline failed: {type(e).__name__}: {str(e)}"
        }

async def generate_batch(prompt_ids: list[str], delay_seconds: float = 2.0) -> list[dict]:
    """
    Generate multiple images with delay between requests.
    DALL-E has rate limits, so we process sequentially with delays.
    """
    results = []
    for i, prompt_id in enumerate(prompt_ids):
        print(f"Generating {i+1}/{len(prompt_ids)}: {prompt_id}")
        result = await generate_and_store_image(prompt_id)
        results.append(result)
        
        # Delay between requests to avoid rate limits
        if i < len(prompt_ids) - 1:
            await asyncio.sleep(delay_seconds)
    
    return results

def generate_all_sync(delay_seconds: float = 2.0) -> list[dict]:
    """Synchronous wrapper for generating all images."""
    prompt_ids = get_all_prompt_ids()
    return asyncio.run(generate_batch(prompt_ids, delay_seconds))

def generate_category_sync(category: str, delay_seconds: float = 2.0) -> list[dict]:
    """Generate all images in a category."""
    prompt_ids = [k for k, v in PROMPTS.items() if v["category"] == category]
    return asyncio.run(generate_batch(prompt_ids, delay_seconds))

# List existing test images in GCS
def list_test_images() -> list[dict]:
    """List all generated test images from GCS."""
    gcs_client = get_gcs_client()
    bucket = gcs_client.bucket(BUCKET_NAME)
    
    images = []
    blobs = bucket.list_blobs(prefix=f"{TEST_FOLDER}/full/")
    
    for blob in blobs:
        filename = blob.name.split("/")[-1]
        prompt_id = "_".join(filename.split("_")[:-2])  # Remove timestamp
        
        thumb_path = f"{TEST_FOLDER}/thumbs/{filename}"
        thumb_blob = bucket.blob(thumb_path)
        
        if prompt_id in PROMPTS:
            images.append({
                "prompt_id": prompt_id,
                "category": PROMPTS[prompt_id]["category"],
                "style": PROMPTS[prompt_id]["style"],
                "prompt": PROMPTS[prompt_id]["prompt"],
                "full_url": blob.public_url,
                "thumb_url": f"https://storage.googleapis.com/{BUCKET_NAME}/{thumb_path}",
                "created_at": blob.time_created.isoformat() if blob.time_created else None
            })
    
    return images
