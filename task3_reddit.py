import logging
import os

from scraper import ScrapingBeeClient

logger = logging.getLogger(__name__)

REDDIT_URL = (
    "https://www.reddit.com/r/neovim/comments/18mro8u/"
    "struggling_to_write_a_simple_remap_function_about/"
)
OUTPUT_HTML = "output/reddit_neovim_post.html"
OUTPUT_SCREENSHOT = "output/reddit_neovim_post.png"


def scrape_reddit(client: ScrapingBeeClient) -> None:
    """
    Scrape a Reddit post including comments and save to an HTML file.
    Uses JS rendering since Reddit is a React SPA that requires JavaScript
    execution to render post content and comments.

    Args:
        client: Reusable ScrapingBeeClient instance
    """
    logger.info("Starting Task 3: Reddit scrape")

    os.makedirs("output", exist_ok=True)

    # Save HTML
    html_content = client.get(REDDIT_URL, params={
        "render_js": "true",
        "premium_proxy": "true",
        "wait": "5000",
    })

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    logger.info(f"HTML saved to {OUTPUT_HTML}")

    # Save screenshot to visually verify comments loaded
    screenshot_content = client.get_raw(REDDIT_URL, params={
        "render_js": "true",
        "premium_proxy": "true",
        "wait": "3000",
        "screenshot": "true",
    })

    with open(OUTPUT_SCREENSHOT, "wb") as f:
        f.write(screenshot_content)
    logger.info(f"Screenshot saved to {OUTPUT_SCREENSHOT}")

    logger.info("Task 3 complete.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    scrape_reddit(ScrapingBeeClient())