import pytest
from unittest.mock import MagicMock, patch
from task3_reddit import scrape_reddit


def test_scrape_reddit_saves_html(tmp_path):
    """scrape_reddit should save HTML content to file."""
    mock_client = MagicMock()
    mock_client.get.return_value = "<html>reddit post</html>"
    mock_client.get_raw.return_value = b"PNG_BYTES"

    with patch("task3_reddit.OUTPUT_HTML", str(tmp_path / "reddit.html")):
        with patch("task3_reddit.OUTPUT_SCREENSHOT", str(tmp_path / "reddit.png")):
            scrape_reddit(mock_client)

    assert (tmp_path / "reddit.html").exists()
    assert (tmp_path / "reddit.html").read_text() == "<html>reddit post</html>"


def test_scrape_reddit_saves_screenshot(tmp_path):
    """scrape_reddit should save screenshot bytes to file."""
    mock_client = MagicMock()
    mock_client.get.return_value = "<html>reddit post</html>"
    mock_client.get_raw.return_value = b"PNG_BYTES"

    with patch("task3_reddit.OUTPUT_HTML", str(tmp_path / "reddit.html")):
        with patch("task3_reddit.OUTPUT_SCREENSHOT", str(tmp_path / "reddit.png")):
            scrape_reddit(mock_client)

    assert (tmp_path / "reddit.png").exists()
    assert (tmp_path / "reddit.png").read_bytes() == b"PNG_BYTES"


def test_scrape_reddit_uses_js_rendering():
    """scrape_reddit should use render_js since Reddit is a React SPA."""
    mock_client = MagicMock()
    mock_client.get.return_value = "<html>reddit post</html>"
    mock_client.get_raw.return_value = b"PNG_BYTES"

    with patch("task3_reddit.OUTPUT_HTML", "/tmp/reddit.html"):
        with patch("task3_reddit.OUTPUT_SCREENSHOT", "/tmp/reddit.png"):
            scrape_reddit(mock_client)

    call_params = mock_client.get.call_args[1]["params"]
    assert call_params["render_js"] == "true"
    assert call_params["wait"] == "5000"