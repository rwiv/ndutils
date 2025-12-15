import asyncio
from typing import Any

from zendriver.core.element import Element
from zendriver.core.tab import Tab

from .query import query_selector_not_null


async def apply_not_null(js_function: str, elem: Element) -> Any:
    ret = await elem.apply(js_function)
    if ret is None:
        raise ValueError(f"{js_function} failed")
    return ret


async def scroll_to_bottom(tab: Tab, step_px: int, delay_ms: int):
    body = await query_selector_not_null("body", tab)
    dest = int(await apply_not_null("e => e.scrollHeight", body))
    for to in range(step_px, dest, step_px):
        await tab.evaluate(f"window.scrollTo(0, {to})")
        await asyncio.sleep(delay_ms / 1000)
