import asyncio
import os
import time
from dataclasses import dataclass

from zendriver.core.connection import ProtocolException
from zendriver.core.element import Element
from zendriver.core.tab import Tab

from .snapshot import screenshot, save_html
from .utils import path_join


@dataclass
class SelectorPair:
    selector: str
    type: str


async def wait_for_selector(
    selectors: list[SelectorPair],
    tab: Tab,
    interval_ms: int | float = 10,
    timeout_ms: int | float = 10 * 1000,
    timout_dir_path: str | None = None,
) -> tuple[Element, str]:
    elapsed = 0
    while elapsed < timeout_ms:
        for pair in selectors:
            elem = await query_selector(pair.selector, tab)
            if elem is not None:
                return elem, pair.type
        await asyncio.sleep(interval_ms / 1000)
        elapsed += interval_ms

    if timout_dir_path is not None:
        current_time_ms = int(time.time() * 1000)
        os.makedirs(timout_dir_path, exist_ok=True)
        await screenshot(tab, path_join(timout_dir_path, f"timeout_{current_time_ms}.png"))
        await save_html(tab, path_join(timout_dir_path, f"timeout_{current_time_ms}.html"))
    raise TimeoutError(f"Timeout waiting for selector")


def get_src(elem: Element) -> str:
    value = elem.attrs["src"]
    if not isinstance(value, str):
        raise ValueError(f"elem is not str: type: {type(value)}, value: {value}")
    return value


def get_href(elem: Element) -> str:
    value = elem.attrs["href"]
    if not isinstance(value, str):
        raise ValueError(f"elem is not str: type: {type(value)}, value: {value}")
    return value


async def query_selector_not_null(selector: str, node: Element | Tab) -> Element:
    elem = await query_selector(selector, node)
    if elem is None:
        raise ValueError(f"{selector} not found")
    return elem


async def query_selector(selector: str, node: Element | Tab) -> Element | None:
    try:
        elem = await node.query_selector(selector)
        if elem is None:
            return None
        if not isinstance(elem, Element):
            raise ValueError(f"{type(elem)} is not Element")
        return elem
    except ProtocolException as e:
        if e.message is not None and "not find" in e.message.lower():
            return None
        raise e


async def query_selector_all(selector: str, node: Element | Tab) -> list[Element]:
    data = await node.query_selector_all(selector)
    if data is None:
        return []

    if not isinstance(data, list):
        raw_list = [data]
    else:
        raw_list = data

    validated_list = []
    for item in raw_list:
        if isinstance(item, Element):
            validated_list.append(item)
        else:
            raise ValueError(f"Invalid item type: {type(item)}")

    return validated_list


async def one_elem(selector: str, node: Element | Tab) -> Element:
    elems = await query_selector_all(selector, node)
    if len(elems) == 0:
        raise ValueError(f"{selector} not found")
    return elems[0]


def find_by_text(elems: list[Element], text: str, is_all: bool = True) -> Element | None:
    for elem in elems:
        if is_all:
            if text in elem.text_all:
                return elem
        else:
            if text in elem.text:
                return elem
    return None
