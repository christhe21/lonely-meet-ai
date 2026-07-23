"""
Lonely Trigger – polls Google Meet DOM for participant count.

Activates only when count == 1 for a configurable duration.
"""

class ParticipantDetector:
    def __init__(self, page, threshold_seconds: float = 5.0):
        self.page = page
        self.threshold_seconds = threshold_seconds

    async def is_lonely(self) -> bool:
        raise NotImplementedError("DOM participant count scraping not yet implemented")

    async def wait_until_lonely(self):
        raise NotImplementedError
