import httpx
from trafilatura import fetch_url, extract
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self):
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=10.0)

    async def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Извлекает заголовок, основной текст и метаданные из URL.
        """
        try:
            downloaded = fetch_url(url)
            if downloaded is None:
                logger.error(f"Failed to download content from {url}")
                return None

            content = extract(downloaded, include_comments=False, include_tables=True)
            
            if not content:
                logger.warning(f"No content extracted from {url}")
                return None

            return {
                "text": content,
                "url": url,
                "title": None 
            }
        except Exception as e:
            logger.exception(f"Error scraping {url}: {e}")
            return None

    async def close(self):
        await self.client.aclose()
