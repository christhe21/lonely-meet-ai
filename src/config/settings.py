"""
Application settings (pydantic-settings planned).
"""

from dataclasses import dataclass

@dataclass
class Settings:
    meet_url: str = ""
    lonely_threshold_seconds: float = 5.0
    deepgram_api_key: str = ""
    openai_api_key: str = ""
    elevenlabs_api_key: str = ""
    persona_name: str = "gordon-ramsay"
    # TODO: load from .env / YAML
