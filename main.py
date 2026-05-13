import argparse
import logging

from scraper import ScrapingBeeClient
from task1_bing import scrape_bing
from task2_amazon import run as run_amazon
from task3_reddit import scrape_reddit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="ScrapingBee assignment — scrape Bing, Amazon, and Reddit."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=[1, 2, 3],
        help="Task to run (1=Bing, 2=Amazon, 3=Reddit). Runs all tasks if not specified."
    )
    return parser.parse_args()


def main() -> None:
    """
    Entry point for the ScrapingBee assignment.
    Runs all tasks or a specific task based on the --task argument.

    Usage:
        python main.py           # runs all tasks
        python main.py --task 1  # runs only Bing
        python main.py --task 2  # runs only Amazon
        python main.py --task 3  # runs only Reddit
    """
    args = parse_args()
    client = ScrapingBeeClient()

    tasks = {
        1: ("Bing search scrape", lambda: scrape_bing(client)),
        2: ("Amazon pagination scrape", run_amazon),
        3: ("Reddit post scrape", lambda: scrape_reddit(client)),
    }

    if args.task:
        name, task_fn = tasks[args.task]
        logger.info(f"Running task {args.task}: {name}")
        task_fn()
    else:
        logger.warning(
            "Running all tasks. This will consume significant API credits. "
            "Use --task 1, --task 2, or --task 3 to run individual tasks."
        )
        for task_num, (name, task_fn) in tasks.items():
            logger.info(f"Running task {task_num}: {name}")
            task_fn()

    logger.info("All done!")


if __name__ == "__main__":
    main()