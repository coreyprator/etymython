# Figure Image Generation Module

Renaissance-style portrait generation for all mythological figures using DALL-E 3.

## Overview

This module generates high-quality Renaissance portrait-style images for each of the 44 mythological figures in the Etymython database. Each figure has a custom prompt with appropriate symbolism and attributes.

## Features

- **44 Custom Prompts**: Each figure has a unique Renaissance allegory-style prompt
- **Dual Image Sizes**: Full 1024×1024 portraits + 80×80 thumbnails
- **GCS Storage**: Organized storage in `gs://etymython-media/figure-images/`
- **Database Integration**: Automatically updates `image_url` field for each figure
- **Batch Generation**: Background task support for generating all images
- **Status Tracking**: Real-time progress monitoring

## Integration Steps

### 1. Add Router to main.py

```python
# In app/main.py, add the import:
from app.image_gen.routes import router as image_gen_router

# Include the router:
app.include_router(image_gen_router)
```

### 2. Install Dependencies

Already included in requirements.txt:
- `openai>=1.0.0`
- `httpx>=0.24.0`
- `Pillow>=10.0.0`
- `google-cloud-storage>=2.0.0`

### 3. Environment Configuration

Required environment variable (or Secret Manager):
- `OPENAI_API_KEY` - For DALL-E 3 API access

## GCS Bucket Structure

```
gs://etymython-media/
└── figure-images/
    ├── full/           # 1024x1024 full portraits
    │   ├── zeus.png
    │   ├── hera.png
    │   └── ...
    └── thumbs/         # 80x80 thumbnails  
        ├── zeus.png
        ├── hera.png
        └── ...
```

## API Endpoints

### GET `/api/v1/images/available-figures`
List all figures with available prompts.

```json
{
  "figures": ["Zeus", "Hera", "Poseidon", ...],
  "figure_types": ["Olympian", "Titan", "Primordial", ...],
  "total": 44
}
```

### GET `/api/v1/images/generated`
List all generated images with URLs.

```json
[
  {
    "figure_name": "Zeus",
    "figure_type": "Olympian",
    "full_url": "https://storage.googleapis.com/...",
    "thumb_url": "https://storage.googleapis.com/...",
    "created_at": "2025-12-25T..."
  }
]
```

### GET `/api/v1/images/for-frontend`
Optimized endpoint for frontend integration - returns simple mapping.

```json
{
  "Zeus": "https://storage.googleapis.com/.../thumbs/zeus.png",
  "Hera": "https://storage.googleapis.com/.../thumbs/hera.png"
}
```

### POST `/api/v1/images/generate/{figure_name}`
Generate image for a single figure.

```bash
curl -X POST "https://etymython-mnovne7bma-uc.a.run.app/api/v1/images/generate/Zeus"
```

### POST `/api/v1/images/generate-all`
Start batch generation of all 44 figures in background.

```bash
curl -X POST "https://etymython-mnovne7bma-uc.a.run.app/api/v1/images/generate-all"
```

**Response:**
```json
{
  "message": "Started batch generation of 44 figures",
  "estimated_cost": "$1.76",
  "estimated_time": "2.2 minutes",
  "status_endpoint": "/api/v1/images/generate-status"
}
```

### GET `/api/v1/images/generate-status`
Check progress of batch generation.

```json
{
  "total": 44,
  "completed": 15,
  "failed": 0,
  "current": "Apollo",
  "in_progress": true,
  "progress_percent": 34.1,
  "errors": []
}
```

### GET `/api/v1/images/stats`
Get generation statistics.

```json
{
  "total_available": 44,
  "total_generated": 44,
  "remaining": 0,
  "progress_percent": 100.0,
  "by_type": {
    "Olympian": 12,
    "Titan": 8,
    "Primordial": 7,
    "Deity": 6,
    "Hero": 7,
    "Mortal": 2
  },
  "estimated_cost_remaining": "$0.00",
  "total_cost_if_all": "$1.76"
}
```

## Usage Examples

### PowerShell - Generate All Images

```powershell
# Start batch generation
Invoke-RestMethod -Uri "https://etymython-mnovne7bma-uc.a.run.app/api/v1/images/generate-all" -Method POST

# Check status periodically
while ($true) {
    $status = Invoke-RestMethod -Uri "https://etymython-mnovne7bma-uc.a.run.app/api/v1/images/generate-status"
    Write-Host "Progress: $($status.completed)/$($status.total) - $($status.progress_percent)%"
    if (-not $status.in_progress) { break }
    Start-Sleep -Seconds 5
}

# View results
Invoke-RestMethod -Uri "https://etymython-mnovne7bma-uc.a.run.app/api/v1/images/stats"
```

### Python - Generate Single Figure

```python
import httpx
import asyncio

async def generate_zeus():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://etymython-mnovne7bma-uc.a.run.app/api/v1/images/generate/Zeus"
        )
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Thumbnail: {result['thumb_url']}")

asyncio.run(generate_zeus())
```

## Cost Estimation

- **Per Image**: $0.04 (DALL-E 3 standard quality, 1024×1024)
- **All 44 Figures**: $1.76
- **HD Quality Option**: $0.08 per image = $3.52 total

## Sample Prompts

### Zeus
> Studio portrait photography styled like a Renaissance allegory: Zeus, the king of the Olympian gods and ruler of sky and thunder, depicted as a powerful regal figure with commanding presence, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: lightning bolt, eagle, oak wreath crown, royal scepter, storm clouds. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text.

### Athena
> Studio portrait photography styled like a Renaissance allegory: Athena, goddess of wisdom, warfare, and crafts, depicted as a wise warrior with intelligent gaze and armor, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: owl companion, Medusa aegis shield, olive branch, helmet with crest, spear, wisdom. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text.

### Medusa
> Studio portrait photography styled like a Renaissance allegory: Medusa, the gorgon whose gaze turns mortals to stone, depicted as a tragically beautiful woman with serpentine features, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: living serpent hair, petrifying stare, grief and rage, stone statues, Athena's curse, transformation. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text.

## Frontend Integration

The updated [frontend/index.html](../../frontend/index.html) fetches image URLs from `/api/v1/images/for-frontend` and applies them as node backgrounds in Cytoscape.

Key changes:
1. Fetch image mapping on load
2. Apply `background-image` style to nodes
3. Keep colored borders for figure type identification
4. Display full portrait in detail panel on click

## Troubleshooting

### Generation Fails
- Check OpenAI API key is valid and has credits
- Verify GCS bucket permissions
- Check logs for rate limit errors

### Images Not Appearing
- Verify blobs are set to public access
- Check CORS configuration on bucket
- Ensure correct bucket name in configuration

### Slow Generation
- Each image takes ~5-10 seconds
- Built-in 2-second delay between requests
- 44 images = ~2-3 minutes total

## Module Structure

```
app/image_gen/
├── __init__.py           # Module exports
├── figure_prompts.py     # 44 Renaissance portrait prompts
├── generator.py          # DALL-E generation + GCS upload
├── routes.py             # FastAPI endpoints
└── README.md             # This file
```

## Next Steps

After deploying:

1. **Test Single Generation**: Generate one figure to verify setup
   ```bash
   curl -X POST ".../api/v1/images/generate/Zeus"
   ```

2. **Start Batch Generation**: Generate all 44 figures
   ```bash
   curl -X POST ".../api/v1/images/generate-all"
   ```

3. **Verify Frontend**: Visit `/app` to see portraits in family tree

4. **Optional**: Enable HD quality in `generator.py` by changing `quality="standard"` to `quality="hd"` ($0.08/image)
