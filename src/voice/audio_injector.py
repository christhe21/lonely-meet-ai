"""
Routes TTS audio into the headless browser's microphone input
so Google Meet treats it as the bot speaking.

Approaches:
- Virtual Audio Cable / BlackHole / PulseAudio null sink
- Web Audio API + MediaStreamTrack injection inside Playwright context
"""

class AudioInjector:
    def __init__(self):
        pass

    async def play(self, audio_bytes: bytes):
        raise NotImplementedError("Audio injection not yet implemented")

    async def mute(self):
        raise NotImplementedError
