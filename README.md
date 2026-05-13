# ScrapingBee Assignment

A web scraping project demonstrating the use of the ScrapingBee API to scrape content from Bing, Amazon, and Reddit.

## Project Structure

scrapingbee_assignment/
├── .env.example # Environment variable template
├── .gitignore
├── README.md
├── requirements.txt # Python dependencies
├── main.py # Entry point — runs all 3 tasks
├── scraper.py # Reusable ScrapingBee client
├── task1_bing.py # Task 1: Bing search scraping
├── task2_amazon.py # Task 2: Amazon pagination (100 pages)
├── task3_reddit.py # Task 3: Reddit JS rendering
└── output/ # Generated files (gitignored)

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

Run all tasks:

```bash
python main.py
```

Or run individual tasks:

```bash
python task1_bing.py
python task2_amazon.py
python task3_reddit.py
```

## Output

Each task saves scraped HTML files to the `output/` directory:

| Task   | Output                                                          |
| ------ | --------------------------------------------------------------- |
| Bing   | `output/bing_pikachu.html`                                      |
| Amazon | `output/amazon_page_001.html` ... `output/amazon_page_100.html` |
| Reddit | `output/reddit_neovim_post.html`                                |

## Tasks

### Task 1 — Bing

Scrapes Bing search results for "pikachu". Uses JS rendering to bypass bot detection and return results as a real browser would see them.

### Task 2 — Amazon

Scrapes the first 100 pages of Amazon.de search results for "Nike". Uses async requests with a concurrency limit to efficiently paginate without getting blocked.

### Task 3 — Reddit

Scrapes a Reddit post including all comments. Uses JS rendering since Reddit is a React SPA that requires JavaScript execution to render content.

## Credits cost estimate

| Task         | Pages | Credits each | Total    |
| ------------ | ----- | ------------ | -------- |
| Bing         | 1     | 5            | ~5       |
| Amazon × 100 | 100   | 5            | ~500     |
| Reddit       | 1     | 5            | ~5       |
| **Total**    |       |              | **~510** |
