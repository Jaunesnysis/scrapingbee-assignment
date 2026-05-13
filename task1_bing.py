import logging
import os

from scraper import ScrapingBeeClient

logger = logging.getLogger(__name__)

BING_URL = (
    "https://www.bing.com/search?q=pikachu&form=QBLH&sp=-1&lq=0"
    "&pq=pikachu&sc=13-7&qs=n&sk=&cvid=7D8FF1A332F7414E9B40B8674FE30D40"
)
OUTPUT_FILE = "output/bing_pikachu.html"


def scrape_bing(client: ScrapingBeeClient) -> None:
    """
    Scrape Bing search results for 'pikachu' and save to an HTML file.
    Uses JS rendering to return results as a real browser would see them.

    Args:
        client: Reusable ScrapingBeeClient instance
    """
    logger.info("Starting Task 1: Bing scrape")

    content = client.get(BING_URL, params={
        "render_js": "true",
        "premium_proxy": "true",
    })

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Task 1 complete. Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_bing(ScrapingBeeClient())