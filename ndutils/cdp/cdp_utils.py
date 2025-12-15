import asyncio
import re
from typing import TypeVar, Generator, Any

from zendriver.cdp.browser import get_version
from zendriver.core.tab import Tab

T = TypeVar("T")


async def send_with_retry(
    tab: Tab,
    cdp_obj: Generator[dict[str, Any], dict[str, Any], T],
    retry_limit: int,
    retry_delay_ms: float = 0,
    with_log: bool = False,
):
    cnt = 0
    while True:
        try:
            return await tab.send(cdp_obj)
        except:
            if cnt >= retry_limit:
                raise
            cnt += 1
            if with_log:
                print(f"Send Retry: cnt={cnt}")
            if retry_delay_ms > 0:
                await asyncio.sleep(retry_delay_ms / 1000)


async def get_user_agent(tab: Tab) -> str:
    tup = await send_with_retry(tab, get_version(), 100, 10)
    user_agent = tup[3]
    if not isinstance(user_agent, str):
        raise ValueError(f"User agent is not a string: {user_agent}")
    regex = re.compile(
        r"(?i)(chrome|firefox|safari|edge|opera|msie|trident|brave|vivaldi|ucbrowser|chromium)"
    )
    if not regex.search(user_agent):
        raise ValueError(f"Invalid user agent: {user_agent}")
    return user_agent
