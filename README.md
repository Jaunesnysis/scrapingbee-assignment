# ScrapingBee Assignment

A web scraping project demonstrating the use of the ScrapingBee API to scrape content from Bing, Amazon, and Reddit.

## Project Structure

```
scrapingbee_assignment/
├── .env.example        # Environment variable template
├── .gitignore
├── README.md
├── requirements.txt    # Python dependencies
├── main.py             # Entry point — runs all 3 tasks
├── scraper.py          # Reusable ScrapingBee client
├── task1_bing.py       # Task 1: Bing search scraping
├── task2_amazon.py     # Task 2: Amazon pagination with duplicate detection
├── task3_reddit.py     # Task 3: Reddit JS rendering
└── output/             # Generated files (gitignored)
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/scrapingbee-assignment.git
cd scrapingbee-assignment
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then open `.env` and replace `your_api_key_here` with your ScrapingBee API key.
Get yours at: https://app.scrapingbee.com/account/usage

## Usage

Run a specific task:

```bash
python main.py --task 1  # Bing
python main.py --task 2  # Amazon
python main.py --task 3  # Reddit
```

Run all tasks (warning: consumes significant API credits):

```bash
python main.py
```

Or run individual task files directly:

```bash
python task1_bing.py
python task2_amazon.py
python task3_reddit.py
```

## Output

Each task saves scraped HTML files and screenshots to the `output/` directory:

| Task   | Output                                                                        |
| ------ | ----------------------------------------------------------------------------- |
| Bing   | `output/bing_pikachu.html`, `output/bing_pikachu.png`                         |
| Amazon | `output/amazon/amazon_page_001.html` ... `output/amazon/amazon_page_00N.html` |
| Reddit | `output/reddit_neovim_post.html`, `output/reddit_neovim_post.png`             |

## Tasks

### Task 1 — Bing

Scrapes Bing search results for "pikachu". Uses JS rendering and premium proxies to bypass bot detection and return results as a real browser would see them. Also saves a screenshot for visual verification.

### Task 2 — Amazon

Scrapes Amazon.de search results for "Nike" with intelligent duplicate detection. The scraper compares product ASINs across pages and stops automatically when Amazon starts returning duplicate results — Amazon.de now returns a maximum of ~8 unique pages for this search query. This avoids wasting API credits on duplicate content while still demonstrating correct pagination logic for up to 100 pages.

### Task 3 — Reddit

Scrapes a Reddit post including all comments. Uses JS rendering since Reddit is a React SPA that requires JavaScript execution to render content. Also saves a screenshot for visual verification.

## Credits cost estimate

| Task                                         | Pages | Credits each | Total   |
| -------------------------------------------- | ----- | ------------ | ------- |
| Bing (HTML + screenshot)                     | 2     | 5            | ~10     |
| Amazon (unique pages only, no premium proxy) | ~8    | 1            | ~8      |
| Reddit (HTML + screenshot)                   | 2     | 5            | ~10     |
| **Total**                                    |       |              | **~28** |
