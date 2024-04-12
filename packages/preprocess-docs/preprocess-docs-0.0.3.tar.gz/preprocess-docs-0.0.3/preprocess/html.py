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
      stripped_text = cur.string.strip()
      if stripped_text:
        child_elem = TextElement(text=cur.string.strip())
        parent.children.append(child_elem)
    elif isinstance(cur, bs4.element.Tag):
      if cur.name == 'a':
        child_elem = LinkElement(text=cur.string.strip(), url=cur.get('href'))
        parent.children.append(child_elem)
      else:
        child_elem = Element(cur.name)
        parent.children.append(child_elem)
        for child in cur.children:
          queue.append((child, child_elem))
  return document
