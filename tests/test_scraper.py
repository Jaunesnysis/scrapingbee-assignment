import pytest
from unittest.mock import MagicMock, patch
from scraper import ScrapingBeeClient


def test_raises_without_api_key():
    """ScrapingBeeClient should raise ValueError if no API key is provided."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="SCRAPINGBEE_API_KEY"):
            ScrapingBeeClient(api_key=None)


def test_get_returns_text_on_success():
    """ScrapingBeeClient.get should return response text on success."""
    mock_response = MagicMock()
    mock_response.text = "<html>result</html>"
    mock_response.raise_for_status = MagicMock()

    with patch("scraper.requests.get", return_value=mock_response):
        client = ScrapingBeeClient(api_key="test_key")
        result = client.get("https://example.com")

    assert result == "<html>result</html>"


def test_get_raw_returns_bytes_on_success():
    """ScrapingBeeClient.get_raw should return bytes on success."""
    mock_response = MagicMock()
    mock_response.content = b"PNG_BYTES"
    mock_response.raise_for_status = MagicMock()

    with patch("scraper.requests.get", return_value=mock_response):
        client = ScrapingBeeClient(api_key="test_key")
        result = client.get_raw("https://example.com")

    assert result == b"PNG_BYTES"


def test_get_retries_on_failure():
    """ScrapingBeeClient.get should retry on HTTP errors."""
    import requests

    mock_response = MagicMock()
    mock_response.text = "<html>result</html>"
    mock_response.raise_for_status = MagicMock(
        side_effect=[
            requests.exceptions.HTTPError("error"),
            requests.exceptions.HTTPError("error"),
            None
        ]
    )

    with patch("scraper.requests.get", return_value=mock_response):
        with patch("scraper.time.sleep"):
            client = ScrapingBeeClient(api_key="test_key", retries=3)
            result = client.get("https://example.com")

    assert result == "<html>result</html>"


def test_get_raises_after_max_retries():
    """ScrapingBeeClient.get should raise RuntimeError after all retries fail."""
    import requests

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock(
        side_effect=requests.exceptions.HTTPError("error")
    )

    with patch("scraper.requests.get", return_value=mock_response):
        with patch("scraper.time.sleep"):
            client = ScrapingBeeClient(api_key="test_key", retries=3)
            with pytest.raises(RuntimeError):
                client.get("https://example.com")