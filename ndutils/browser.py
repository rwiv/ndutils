import asyncio

from nodriver.core.browser import Browser


async def browser_stop(browser: Browser, delay_sec: float = 1.0):
    if browser.connection:
        await browser.connection.disconnect()
    browser.stop()
    await asyncio.sleep(delay_sec)
