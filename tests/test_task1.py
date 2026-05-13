import pytest
from unittest.mock import MagicMock, patch
import os
from task1_bing import scrape_bing


def test_scrape_bing_saves_html(tmp_path):
    """scrape_bing should save HTML content to file."""
    mock_client = MagicMock()
    mock_client.get.return_value = "<html>bing results</html>"
    mock_client.get_raw.return_value = b"PNG_BYTES"

    with patch("task1_bing.OUTPUT_HTML", str(tmp_path / "bing.html")):
        with patch("task1_bing.OUTPUT_SCREENSHOT", str(tmp_path / "bing.png")):
            scrape_bing(mock_client)

    assert (tmp_path / "bing.html").exists()
    assert (tmp_path / "bing.html").read_text() == "<html>bing results</html>"


def test_scrape_bing_saves_screenshot(tmp_path):
    """scrape_bing should save screenshot bytes to file."""
    mock_client = MagicMock()
    mock_client.get.return_value = "<html>bing results</html>"
    mock_client.get_raw.return_value = b"PNG_BYTES"

    with patch("task1_bing.OUTPUT_HTML", str(tmp_path / "bing.html")):
        with patch("task1_bing.OUTPUT_SCREENSHOT", str(tmp_path / "bing.png")):
            scrape_bing(mock_client)

    assert (tmp_path / "bing.png").exists()
    assert (tmp_path / "bing.png").read_bytes() == b"PNG_BYTES"


def test_scrape_bing_calls_api_with_correct_params():
    """scrape_bing should call ScrapingBee with render_js and premium_proxy."""
    mock_client = MagicMock()
    mock_client.get.return_value = "<html>bing results</html>"
    mock_client.get_raw.return_value = b"PNG_BYTES"

    with patch("task1_bing.OUTPUT_HTML", "/tmp/bing.html"):
        with patch("task1_bing.OUTPUT_SCREENSHOT", "/tmp/bing.png"):
            scrape_bing(mock_client)

    call_params = mock_client.get.call_args[1]["params"]
    assert call_params["render_js"] == "true"
    assert call_params["premium_proxy"] == "true"
    assert call_params["wait"] == "3000"