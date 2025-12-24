# Image Test Module Integration

## Add to main.py

Add these lines to your existing `app/main.py`:

```python
# At the top with other imports:
from fastapi.responses import FileResponse
from app.image_test.routes import router as image_test_router

# After creating the FastAPI app, add the router:
app.include_router(image_test_router)

# Add the gallery endpoint (near your other frontend routes):
@app.get("/gallery")
async def gallery():
    return FileResponse("frontend/gallery.html")
```

## Add to requirements.txt

```
httpx>=0.24.0
Pillow>=10.0.0
```

## Environment Variables

Make sure these are set (or available via Secret Manager):
- `OPENAI_API_KEY` - For DALL-E 3 image generation

## GCS Bucket Setup

The bucket `gs://etymython-media` should already exist. The module will create:
- `style-test/full/` - Full 1024x1024 images
- `style-test/thumbs/` - 80x80 thumbnails

Make sure the bucket allows public read access for the images, or configure signed URLs.

## Usage

1. Deploy the updated app
2. Go to https://etymython-mnovne7bma-uc.a.run.app/gallery
3. Click "Generate Images" to start creating test images
4. Rate each style with stars (1-5)
5. Use filters and sorting to compare
6. Click "View Rankings" to see top-rated styles
7. Click "Export" to download your ratings as JSON

## API Endpoints

- `GET /api/v1/image-test/prompts` - All prompts
- `GET /api/v1/image-test/images` - Generated images
- `GET /api/v1/image-test/stats` - Generation statistics
- `POST /api/v1/image-test/generate/{prompt_id}` - Generate single image
- `GET /gallery` - The rating gallery UI

## Cost Estimate

- 53 prompts × $0.04 per image = ~$2.12 total
- HD quality option: $0.08 per image = ~$4.24 total
