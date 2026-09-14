from typing import Any
from app.adapters.base import BaseAdapter
import httpx

class HTTPAdapter(BaseAdapter):

    @property
    def step_type(self) -> str:
        return "http"

    def execute(
            self, 
            config: dict[str, Any],
    ) -> dict[str, Any]:

        method = config.get("method", "GET").upper()
        url = config.get("url")

        if not url:
            raise ValueError("HTTP step requires a URL")

        headers = config.get("headers")
        params = config.get("params")
        json_body = config.get("json")
        timeout = config.get("timeout", 30)

        supported_methods = {
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        }

        if method not in supported_methods:
            raise ValueError(f"Unsupported HTTP method: {method}")

        with httpx.Client(
            timeout=timeout,
            follow_redirects=True,
        ) as client:

            response = client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
            )
            response.raise_for_status()
        

        return {
            "status": "success",
            "http_status": response.status_code,
            "url": str(response.url),
            "method": method,
            "headers": dict(response.headers),
            "body": response.text,            
        }