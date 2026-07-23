"""
Joiner component – launches headless browser and joins Google Meet.

Primary path: Playwright.
Alternative (future): Recall.ai / Meeting Baas managed bots.
"""

class PlaywrightJoiner:
    def __init__(self, meet_url: str):
        self.meet_url = meet_url

    async def join(self):
        raise NotImplementedError("Playwright join logic not yet implemented")

    async def leave(self):
        raise NotImplementedError
