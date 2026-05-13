import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from task2_amazon import get_content_hash, build_amazon_url, scrape_amazon


def test_build_amazon_url_page_1():
    """build_amazon_url should return correct URL for page 1."""
    url = build_amazon_url(1)
    assert "page=1" in url
    assert "k=Nike" in url
    assert "start=0" in url


def test_build_amazon_url_page_5():
    """build_amazon_url should calculate correct offset for page 5."""
    url = build_amazon_url(5)
    assert "page=5" in url
    assert "start=64" in url


def test_get_content_hash_detects_duplicates():
    """get_content_hash should return same hash for pages with same ASINs."""
    content_a = 'data-asin="B001234567" data-asin="B009876543"'
    content_b = 'data-asin="B001234567" data-asin="B009876543" different_timestamp="123"'

    assert get_content_hash(content_a) == get_content_hash(content_b)


def test_get_content_hash_differs_for_different_asins():
    """get_content_hash should return different hash for pages with different ASINs."""
    content_a = 'data-asin="B001234567"'
    content_b = 'data-asin="B009999999"'

    assert get_content_hash(content_a) != get_content_hash(content_b)


def test_get_content_hash_empty_page():
    """get_content_hash should handle pages with no ASINs gracefully."""
    content = "<html>No results found</html>"
    result = get_content_hash(content)
    assert isinstance(result, str)
    assert len(result) == 32  # MD5 hash length


@pytest.mark.asyncio
async def test_scrape_amazon_stops_on_duplicate():
    """scrape_amazon should stop scraping when duplicate ASINs are detected."""
    unique_content = 'data-asin="B001234567" data-asin="B009876543"'
    duplicate_content = 'data-asin="B001234567" data-asin="B009876543"'

    call_count = 0

    async def mock_scrape_page(session, semaphore, page):
        nonlocal call_count
        call_count += 1
        if page == 1:
            return page, unique_content
        return page, duplicate_content

    with patch("task2_amazon.scrape_page", side_effect=mock_scrape_page):
        with patch("task2_amazon.open", MagicMock()):
            with patch("task2_amazon.os.makedirs", MagicMock()):
                await scrape_amazon()

    assert call_count <= 10