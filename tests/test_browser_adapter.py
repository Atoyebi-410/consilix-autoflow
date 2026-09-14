from app.adapters.browser import BrowserAdapter


def test_browser_navigate():
    adapter = BrowserAdapter()

    result = adapter.execute(
        {
            "url": "https://example.com",
            "action": "navigate",
        }
    )

    assert result["status"] == "success"
    assert result["url"] == "https://example.com/"
    assert "Example" in result["title"]