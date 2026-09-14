from typing import Any
from playwright.sync_api import sync_playwright
from app.adapters.base import BaseAdapter

def _require_config(
    config: dict[str, Any],
    key: str,
) -> Any:
    value = config.get(key)

    if value is None or value == "":
        raise ValueError(
            f"Browser configuration requires '{key}'"
        )

    return value


class BrowserAdapter(BaseAdapter):

    @property
    def step_type(self) -> str:
        return "browser"

    def execute(
        self,
        config: dict[str, Any],
    ) -> dict[str, Any]:

        url = _require_config(
                config,
                "url",
            )
        action = config.get("action", "navigate")

        if not url:
            raise ValueError(
                "Browser step requires a URL"
            )

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
            )

            page = browser.new_page()
            try:
                page.goto(
                    url,
                    wait_until="domcontentloaded",
                )
                if action == "navigate":
                    return {
                        "status": "success",
                        "action": "navigate",
                        "url": page.url,
                        "title": page.title(),
                    }

                if action == "click":
                    selector = _require_config(
                            config,
                            "selector",
                        )

                    if not selector:
                        raise ValueError(
                            "Click action requires a selector"
                        )

                    page.click(selector)

                    return {
                        "status": "success",
                        "action": "click",
                        "selector": selector,
                        "url": page.url,
                    }

                if action == "fill":
                    selector = config.get("selector")
                    value = config.get("value")

                    if not selector:
                        raise ValueError(
                            "Fill action requires a selector"
                        )

                    if value is None:
                        raise ValueError(
                            "Fill action requires a value"
                        )

                    page.fill(
                        selector,
                        value,
                    )

                    return {
                        "status": "success",
                        "action": "fill",
                        "selector": selector,
                    }

                if action == "extract_text":
                    selector = config.get("selector")

                    if not selector:
                        raise ValueError(
                            "Extract action requires a selector"
                        )

                    text = page.locator(
                        selector
                    ).inner_text()

                    return {
                        "status": "success",
                        "action": "extract_text",
                        "selector": selector,
                        "text": text,
                    }

                raise ValueError(
                    f"Unsupported browser action: {action}"
                )

            finally:
                browser.close()