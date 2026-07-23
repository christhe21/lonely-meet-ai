"""
Application settings.

Supports both cloud and local LLMs via OpenAI-compatible endpoints
(Ollama, LM Studio, vLLM, llama.cpp server, etc.).
"""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Settings:
    # Meeting
    meet_url: str = ""
    lonely_threshold_seconds: float = 5.0

    # STT (cloud for now; local Whisper later)
    deepgram_api_key: str = ""

    # LLM provider selection
    # Options: "openai" | "anthropic" | "ollama" | "openai_compatible"
    llm_provider: Literal["openai", "anthropic", "ollama", "openai_compatible"] = "ollama"

    # Model name (e.g. "gpt-4o", "claude-3-5-sonnet", "llama3.1", "qwen2.5", etc.)
    llm_model: str = "llama3.1"

    # Base URL for local / OpenAI-compatible servers
    # Ollama default: http://localhost:11434/v1
    # LM Studio default: http://localhost:1234/v1
    llm_base_url: str = "http://localhost:11434/v1"

    # API keys (only needed for cloud providers)
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # TTS
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""

    # Persona
    persona_name: str = "gordon-ramsay"

    # Optional: temperature, max_tokens, etc.
    llm_temperature: float = 0.7
    llm_max_tokens: int = 256

    # TODO: replace with pydantic-settings + .env loading
