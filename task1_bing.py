import logging
import os

from scraper import ScrapingBeeClient

logger = logging.getLogger(__name__)

BING_URL = (
    "https://www.bing.com/search?q=pikachu&form=QBLH&sp=-1&lq=0"
    "&pq=pikachu&sc=13-7&qs=n&sk=&cvid=7D8FF1A332F7414E9B40B8674FE30D40"
)
OUTPUT_HTML = "output/bing_pikachu.html"
OUTPUT_SCREENSHOT = "output/bing_pikachu.png"


def scrape_bing(client: ScrapingBeeClient) -> None:
    """
    Scrape Bing search results for 'pikachu' and save to an HTML file.
    Also saves a screenshot to visually verify the results.
    Uses JS rendering to return results as a real browser would see them.

    Args:
        client: Reusable ScrapingBeeClient instance
    """
    logger.info("Starting Task 1: Bing scrape")

    os.makedirs("output", exist_ok=True)

    # Save HTML
    html_content = client.get(BING_URL, params={
        "render_js": "true",
        "premium_proxy": "true",
        "wait": "3000",
    })

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    logger.info(f"HTML saved to {OUTPUT_HTML}")

# Save screenshot (returned as raw bytes)
    screenshot_response = client.get_raw(BING_URL, params={
        "render_js": "true",
        "premium_proxy": "true",
        "screenshot": "true",
        "wait": "3000",
    })

    with open(OUTPUT_SCREENSHOT, "wb") as f:
        f.write(screenshot_response)
    logger.info(f"Screenshot saved to {OUTPUT_SCREENSHOT}")

    logger.info("Task 1 complete.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    scrape_bing(ScrapingBeeClient())