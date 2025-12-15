import json

from nodriver.core.browser import Browser
from nodriver.core.tab import Tab

from .cookie import Cookie


async def get_cookie_headers_by_tab(tab: Tab):
    cookie_str = await get_cookie_string_by_tab(tab)
    return {"Cookie": cookie_str}


async def get_cookie_string_by_tab(tab: Tab):
    return to_cookie_string(await get_current_cookies(tab))


def to_cookie_string(cookies: list[Cookie]) -> str:
    result = ""
    for i, cookie in enumerate(cookies):
        result += f"{cookie.name}={cookie.value}"
        if i != len(cookies) - 1:
            result += "; "
    return result


async def get_current_cookies(target: Tab | Browser) -> list[Cookie]:
    browser: Browser | None = None
    if isinstance(target, Tab):
        browser = target.browser
    elif isinstance(target, Browser):
        browser = target
    if browser is None:
        raise Exception("browser is None")
    cookies: list[network.Cookie] = await browser.cookies.get_all()  # type: ignore
    return [Cookie(**c.to_json()) for c in cookies]


async def save_cookies(browser: Browser, json_path: str):
    cookies = [c.model_dump(mode="json") for c in await get_current_cookies(browser)]
    with open(json_path, "w") as file:
        file.write(json.dumps(cookies, indent=2))


async def load_cookies(browser: Browser, json_path: str):
    with open(json_path, "rb") as file:
        cookies: list[dict] = json.loads(file.read())
        valid_cookies = [Cookie(**c).to_cookie_param() for c in cookies]
        await browser.cookies.set_all(valid_cookies)
