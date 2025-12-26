"""
AI content generation using OpenAI GPT-4.
Generates origin stories and fun facts for mythological figures.
"""

import os
import json
from openai import AsyncOpenAI
from typing import Dict, List

async def get_openai_client() -> AsyncOpenAI:
    """Get OpenAI client with API key from Secret Manager or environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            name = "projects/etymython-project/secrets/openai-api-key/versions/latest"
            response = client.access_secret_version(request={"name": name})
            api_key = response.payload.data.decode("UTF-8").strip()
        except Exception as e:
            raise ValueError(f"OPENAI_API_KEY not found: {e}")
    
    return AsyncOpenAI(api_key=api_key)


async def generate_origin_story(figure: Dict) -> str:
    """Generate an engaging origin story for a mythological figure."""
    
    client = await get_openai_client()
    
    prompt = f"""Write a compelling 2-3 paragraph origin story for {figure['english_name']} ({figure.get('greek_name', '')}) from Greek mythology.

Figure details:
- Role: {figure.get('role', 'Unknown')}
- Domain: {figure.get('domain', 'Unknown')}
- Symbols: {figure.get('symbols', 'Unknown')}
- Type: {figure.get('figure_type', 'Unknown')}

Requirements:
- Be accurate to classical Greek mythology (Hesiod, Homer, Ovid)
- Include their birth/creation and key mythological events
- Mention their parents if known
- Keep it engaging but educational
- 150-250 words
- Do NOT include the figure's name in the first sentence - start with an interesting hook"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a classical mythology scholar writing engaging educational content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()


async def generate_fun_facts(figure: Dict) -> List[Dict]:
    """Generate 3-5 fun facts about a mythological figure."""
    
    client = await get_openai_client()
    
    prompt = f"""Generate 4 fascinating fun facts about {figure['english_name']} ({figure.get('greek_name', '')}) from Greek mythology.

Figure details:
- Role: {figure.get('role', 'Unknown')}
- Domain: {figure.get('domain', 'Unknown')}
- Symbols: {figure.get('symbols', 'Unknown')}

Requirements:
- Include at least ONE etymology/linguistic fact (English words derived from their name)
- Include at least ONE surprising or lesser-known mythological fact
- Include at least ONE cultural impact fact (art, literature, modern references)
- Each fact should be 1-2 sentences
- Be accurate to classical sources
- Make them memorable and "did you know?" worthy

Return as JSON array with objects containing:
- "content": the fact text
- "category": one of "linguistic", "mythological", "cultural", "historical"
- "surprise_factor": 1-5 (how surprising/memorable)"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a classical mythology scholar. Return ONLY valid JSON, no markdown."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.7
    )
    
    try:
        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])  # Remove first and last lines
            if content.startswith("json"):
                content = content[4:].strip()
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse fun facts JSON: {e}")
