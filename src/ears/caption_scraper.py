"""
Fallback / alternative: scrape Google Meet live Closed Captions from the DOM.
Easier but less accurate and more fragile than true audio STT.
"""

class CaptionScraper:
    def __init__(self, page):
        self.page = page

    async def get_latest_captions(self) -> str:
        raise NotImplementedError("Caption DOM scraping not yet implemented")
