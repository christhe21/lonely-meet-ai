"""
Brain – LLM + persona system prompt.

Supports:
- Cloud: OpenAI, Anthropic
- Local: Ollama, LM Studio, any OpenAI-compatible endpoint
"""

from typing import Literal
import os


class LLMPersona:
    def __init__(
        self,
        system_prompt: str,
        provider: Literal["openai", "anthropic", "ollama", "openai_compatible"] = "ollama",
        model: str = "llama3.1",
        base_url: str = "http://localhost:11434/v1",
        api_key: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 256,
    ):
        self.system_prompt = system_prompt
        self.provider = provider
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "ollama")  # Ollama ignores key
        self.temperature = temperature
        self.max_tokens = max_tokens

        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        if self.provider in ("openai", "ollama", "openai_compatible"):
            from openai import AsyncOpenAI

            # Ollama and most local servers are OpenAI-compatible
            self._client = AsyncOpenAI(
                base_url=self.base_url if self.provider != "openai" else None,
                api_key=self.api_key if self.provider == "openai" else (self.api_key or "ollama"),
            )
            return self._client

        if self.provider == "anthropic":
            from anthropic import AsyncAnthropic

            self._client = AsyncAnthropic(api_key=self.api_key)
            return self._client

        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def generate_response(
        self,
        transcript: str,
        history: list[dict] | None = None,
    ) -> str:
        """
        Generate a persona-aligned response to the user's transcript.

        history format (optional): list of {"role": "user"|"assistant", "content": "..."}
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": transcript})

        client = self._get_client()

        if self.provider in ("openai", "ollama", "openai_compatible"):
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()

        if self.provider == "anthropic":
            # Anthropic expects system separately
            system = self.system_prompt
            anthropic_messages = [m for m in messages if m["role"] != "system"]
            response = await client.messages.create(
                model=self.model,
                system=system,
                messages=anthropic_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.content[0].text.strip()

        raise ValueError(f"Unsupported provider: {self.provider}")
