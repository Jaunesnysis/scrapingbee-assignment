import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

SCRAPINGBEE_BASE_URL = "https://app.scrapingbee.com/api/v1/"


class ScrapingBeeClient:
    def __init__(self, api_key: str = None, retries: int = 3, backoff_factor: float = 2.0):
        self.api_key = api_key or os.getenv("SCRAPINGBEE_API_KEY")
        self.retries = retries
        self.backoff_factor = backoff_factor

        if not self.api_key:
            raise ValueError("ScrapingBee API key not found. Set SCRAPINGBEE_API_KEY in your .env file.")

    def get(self, url: str, params: dict = None) -> str:
        """
        Make a GET request via ScrapingBee API with retry logic.

        Args:
            url: Target URL to scrape
            params: Additional ScrapingBee parameters (e.g. render_js, premium_proxy)

        Returns:
            Response content as string
        """
        request_params = {
            "api_key": self.api_key,
            "url": url,
            **(params or {})
        }

        for attempt in range(1, self.retries + 1):
            try:
                logger.info(f"Scraping (attempt {attempt}/{self.retries}): {url}")
                response = requests.get(SCRAPINGBEE_BASE_URL, params=request_params)
                response.raise_for_status()
                logger.info(f"Success: {url}")
                return response.text

            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP error on attempt {attempt}: {e}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request error on attempt {attempt}: {e}")

            if attempt < self.retries:
                wait = self.backoff_factor ** attempt
                logger.info(f"Retrying in {wait:.1f}s...")
                time.sleep(wait)

        raise RuntimeError(f"Failed to scrape {url} after {self.retries} attempts.")