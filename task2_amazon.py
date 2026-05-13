import asyncio
import hashlib
import logging
import os
import re

import aiohttp
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

AMAZON_BASE_URL = "https://www.amazon.de/s"
SCRAPINGBEE_BASE_URL = "https://app.scrapingbee.com/api/v1/"
API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
TOTAL_PAGES = 100
CONCURRENCY_LIMIT = 5
OUTPUT_DIR = "output/amazon"


def build_amazon_url(page: int) -> str:
    """Build Amazon search URL for a given page number."""
    offset = (page - 1) * 16
    return f"{AMAZON_BASE_URL}?k=Nike&page={page}&s=relevanceblender&ref=nb_sb_noss&start={offset}"


def get_content_hash(content: str) -> str:
    """
    Generate a hash based only on product ASINs to detect duplicate pages.
    Amazon injects dynamic content (timestamps, session IDs) that changes
    between requests, so we compare only the stable product identifiers.

    Args:
        content: HTML content of the page

    Returns:
        MD5 hash of sorted ASIN list
    """
    asins = sorted(set(re.findall(r'data-asin="([A-Z0-9]{10})"', content)))
    return hashlib.md5(",".join(asins).encode("utf-8")).hexdigest()


async def scrape_page(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    page: int
) -> tuple:
    """
    Scrape a single Amazon search result page.

    Args:
        session: Shared aiohttp session
        semaphore: Concurrency limiter
        page: Page number to scrape

    Returns:
        Tuple of (page_number, content or None if failed)
    """
    url = build_amazon_url(page)
    params = {
        "api_key": API_KEY,
        "url": url,
        "render_js": "false",
        "premium_proxy": "false",
        "country_code": "de",
    }

    async with semaphore:
        for attempt in range(1, 4):
            try:
                logger.info(f"Scraping page {page} (attempt {attempt}/3)")
                async with session.get(SCRAPINGBEE_BASE_URL, params=params) as response:
                    response.raise_for_status()
                    content = await response.text()
                    logger.info(f"Page {page} fetched successfully")
                    return page, content

            except aiohttp.ClientResponseError as e:
                logger.warning(f"Page {page} HTTP error on attempt {attempt}: {e}")
            except aiohttp.ClientError as e:
                logger.warning(f"Page {page} request error on attempt {attempt}: {e}")

            if attempt < 3:
                wait = 2.0 ** attempt
                logger.info(f"Page {page} retrying in {wait:.1f}s...")
                await asyncio.sleep(wait)

        logger.error(f"Page {page} failed after 3 attempts.")
        return page, None


async def scrape_amazon() -> None:
    """
    Scrape Amazon.de Nike search results with duplicate detection.

    Scrapes pages sequentially in batches, stopping early if duplicate
    content is detected — indicating Amazon has no more unique pages.

    Note: Amazon.de search for 'Nike' returns a maximum of ~7 pages of
    unique results. Pages beyond that repeat the last page's content.
    This scraper detects that and stops early rather than wasting API
    credits on duplicate content.
    """
    logger.info("Starting Task 2: Amazon pagination with duplicate detection")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    seen_hashes = {}
    saved_count = 0
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with aiohttp.ClientSession() as session:
        for batch_start in range(1, TOTAL_PAGES + 1, CONCURRENCY_LIMIT):
            batch = range(batch_start, min(batch_start + CONCURRENCY_LIMIT, TOTAL_PAGES + 1))
            tasks = [scrape_page(session, semaphore, page) for page in batch]
            results = await asyncio.gather(*tasks)

            duplicate_detected = False

            for page, content in sorted(results, key=lambda x: x[0]):
                if content is None:
                    continue

                content_hash = get_content_hash(content)

                if content_hash in seen_hashes:
                    logger.warning(
                        f"Page {page} is a duplicate of page {seen_hashes[content_hash]}. "
                        f"Amazon has no more unique results. Stopping at page {page - 1}."
                    )
                    duplicate_detected = True
                    break

                seen_hashes[content_hash] = page
                filepath = os.path.join(OUTPUT_DIR, f"amazon_page_{page:03d}.html")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                saved_count += 1
                logger.info(f"Page {page} saved to {filepath}")

            if duplicate_detected:
                break

    logger.info(
        f"Task 2 complete. Saved {saved_count} unique pages to {OUTPUT_DIR}. "
        f"Amazon returned {saved_count} unique pages out of {TOTAL_PAGES} requested."
    )


def run() -> None:
    """Entry point for Task 2."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    asyncio.run(scrape_amazon())


if __name__ == "__main__":
    run()