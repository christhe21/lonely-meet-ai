"""
Deepgram streaming STT client.

Alternative: Gladia, or scraping Google Meet live captions from DOM.
"""

class DeepgramSTT:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def start_stream(self):
        raise NotImplementedError("Deepgram streaming not yet implemented")

    async def stop_stream(self):
        raise NotImplementedError
