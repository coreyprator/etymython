"""
Audio generation using Google Cloud Text-to-Speech API.
Generates pronunciation audio for Greek names.
"""

from google.cloud import texttospeech
from google.cloud import storage
import os
from typing import Optional

BUCKET_NAME = "etymython-media"
AUDIO_FOLDER = "audio"

async def generate_pronunciation_audio(
    greek_name: str,
    english_name: str,
    project_id: str = "etymython-project"
) -> str:
    """
    Generate pronunciation audio for a Greek name using Google Cloud TTS.
    
    Args:
        greek_name: The Greek name to pronounce (e.g., "Ἀφροδίτη")
        english_name: English name for filename (e.g., "Aphrodite")
        project_id: GCP project ID
        
    Returns:
        Public URL of the uploaded audio file
    """
    # Initialize clients
    tts_client = texttospeech.TextToSpeechClient()
    storage_client = storage.Client(project=project_id)
    
    # Configure TTS
    synthesis_input = texttospeech.SynthesisInput(text=greek_name)
    
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
    
    # Generate audio
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Upload to GCS
    filename = f"{english_name.lower().replace(' ', '_')}.mp3"
    blob_name = f"{AUDIO_FOLDER}/{filename}"
    
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(response.audio_content, content_type="audio/mpeg")
    blob.make_public()
    
    return blob.public_url


async def delete_pronunciation_audio(audio_url: str, project_id: str = "etymython-project"):
    """
    Delete an audio file from GCS.
    
    Args:
        audio_url: Full URL of the audio file
        project_id: GCP project ID
    """
    # Extract blob name from URL
    # Format: https://storage.googleapis.com/etymython-media/audio/filename.mp3
    if "etymython-media" in audio_url:
        blob_name = audio_url.split("etymython-media/")[1]
        
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        if blob.exists():
            blob.delete()
