import base64

from zendriver import cdp
from zendriver.cdp.page import Viewport
from zendriver.core.element import Element
from zendriver.core.tab import Tab


async def save_html(tab: Tab, file_path: str):
    html = await tab.get_content()
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)


async def screenshot(tab: Tab, file_path: str):
    await tab.save_screenshot(file_path, "jpeg", True)


async def screenshot_elem(
    tab: Tab,
    elem: Element,
    file_path: str,
    format_: str = "png",
    with_margin: bool = True,
):
    box_model = await tab.send(cdp.dom.get_box_model(backend_node_id=elem.backend_node_id))
    content = box_model.content
    if with_margin:
        content = box_model.margin
    clip = Viewport(
        x=content[0], y=content[1], width=content[2] - content[0], height=content[5] - content[1], scale=1
    )

    gen = cdp.page.capture_screenshot(format_=format_, capture_beyond_viewport=True, clip=clip)
    data = await tab.send(gen)
    if not data:
        raise Exception("could not take screenshot")
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(data))
