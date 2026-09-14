from app.adapters.http import HTTPAdapter

def test_http_get():

    adapter = HTTPAdapter()

    result = adapter.execute(
        {
            "url": "https://example.com",
            "method": "GET",
        }
    )

    assert result["status"] == "success"
    assert result["http_status"] == 200
    assert result["method"] == "GET"
    assert "Example Domain" in result["body"]

def test_http_post():
    adapter = HTTPAdapter()

    result = adapter.execute(
        {
            "url": "https://httpbin.org/post",
            "method": "POST",
            "json": {
                "name": "Consilix AutoFlow",
                "type": "automation",
            }
        }
    )

    assert result["status"] == "success"
    assert result["http_status"] == 200
    assert result["method"] == "POST"