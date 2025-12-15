import asyncio

from nodriver.core.browser import Browser


async def browser_stop(browser: Browser, delay_sec: float = 0.5):
    browser.stop()
    await asyncio.sleep(delay_sec)
