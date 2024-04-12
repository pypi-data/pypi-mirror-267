from .element import Element, LinkElement, TextElement
from collections import deque
import bs4
from bs4 import BeautifulSoup

def html(page_content) -> Element:
  html_tag = BeautifulSoup(page_content, "html5lib")
  document = Element("Page")
  visited = set()
  queue = deque([(html_tag, document)])
  while queue:
    cur, parent = queue.popleft()
    if cur in visited:
      continue
    visited.add(cur)
    if isinstance(cur, bs4.element.NavigableString):
      if cur.string is None or cur.string.strip() == "":
        continue
      child_elem = TextElement(text=cur.string.strip())
      parent.children.append(child_elem)
    elif isinstance(cur, bs4.element.Tag):
      if cur.name == 'a':
        text = None if cur.string is None else cur.string.strip()
        child_elem = LinkElement(text=text, url=cur.get('href'))
        parent.children.append(child_elem)
      else:
        child_elem = Element(cur.name)
        parent.children.append(child_elem)

      for child in cur.children:
        queue.append((child, child_elem))
  return document
