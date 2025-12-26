"""
Generate Greek pronunciation audio for all mythological figures using Google Cloud TTS.
Uploads to gs://etymython-media/audio/ and updates database.
"""

import os
from google.cloud import texttospeech
from google.cloud import storage
import requests

# Configuration
BUCKET_NAME = "etymython-media"
AUDIO_FOLDER = "audio"
PROJECT_ID = "etymython-project"
API_BASE = "https://etymython-mnovne7bma-uc.a.run.app"

def generate_audio(text: str, filename: str) -> bytes:
    """Generate audio using Google Cloud TTS with Greek voice."""
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    # Use Greek voice for authentic pronunciation
    voice = texttospeech.VoiceSelectionParams(
        language_code="el-GR",  # Greek
        name="el-GR-Wavenet-A",  # High-quality Wavenet voice
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.85,  # Slightly slower for learning
        pitch=0.0
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    return response.audio_content

def upload_to_gcs(audio_bytes: bytes, blob_name: str) -> str:
    """Upload audio to Google Cloud Storage and return public URL."""
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    
    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")
    blob.make_public()
    
    return blob.public_url

def update_database_via_api(figure_id: int, audio_url: str):
    """Update the pronunciation_audio_url for a figure via API."""
    response = requests.put(
        f"{API_BASE}/api/v1/figures/{figure_id}",
        json={"pronunciation_audio_url": audio_url}
    )
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

def main():
    # Get all figures with Greek names
    response = requests.get(f"{API_BASE}/api/v1/figures?limit=100")
    figures = response.json()
    
    # Filter figures with Greek names
    figures_with_greek = [
        f for f in figures 
        if f.get("greek_name") and f["greek_name"].strip()
    ]
    
    print(f"Generating audio for {len(figures_with_greek)} figures...\n")
    
    success_count = 0
    error_count = 0
    
    for figure in figures_with_greek:
        try:
            figure_id = figure["id"]
            english_name = figure["english_name"]
            greek_name = figure["greek_name"]
            
            # Generate filename
            filename = f"{english_name.lower().replace(' ', '_')}.mp3"
            blob_name = f"{AUDIO_FOLDER}/{filename}"
            
            print(f"  {english_name} ({greek_name})...", end=" ", flush=True)
            
            # Generate audio
            audio_bytes = generate_audio(greek_name, filename)
            
            # Upload to GCS
            audio_url = upload_to_gcs(audio_bytes, blob_name)
            
            # Update database via API
            update_database_via_api(figure_id, audio_url)
            
            print(f"✓")
            print(f"    URL: {audio_url}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"✓ Audio Generation Complete!")
    print(f"Success: {success_count} files")
    print(f"Errors: {error_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
