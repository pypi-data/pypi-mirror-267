from .element import Element, LinkElement
from typing import Optional, Union
import bs4
from bs4 import BeautifulSoup


def html(page_content) -> Optional[Union[Element, str]]:
    html_tag = BeautifulSoup(page_content, "html5lib", from_encoding="utf8")
    return _convert_html_recursive(html_tag)


def _convert_html_recursive(bse) -> Optional[Union[Element, str]]:
    if bse is None:
        return None
    if isinstance(bse, bs4.element.NavigableString):
        text = bse.strip()
        return None if text == "" else text
    if bse.name == "a":
        element = LinkElement(bse.name, url=bse.get("href"))
    else:
        element = Element(name=bse.name)
    for child in bse.children:
        child_element = _convert_html_recursive(child)
        if child_element is not None:
            element.children.append(child_element)
    return element
