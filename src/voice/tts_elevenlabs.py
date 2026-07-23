"""
Text-to-Speech via ElevenLabs (or OpenAI Audio as alternative).
"""

class ElevenLabsTTS:
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id

    async def synthesize(self, text: str) -> bytes:
        """Return raw audio bytes (e.g. mp3 or pcm)."""
        raise NotImplementedError("ElevenLabs TTS not yet implemented")
