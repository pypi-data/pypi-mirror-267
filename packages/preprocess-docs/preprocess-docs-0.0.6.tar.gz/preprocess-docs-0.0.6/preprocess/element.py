import uuid
from typing import Union


class ElementMetadata:
    pass


class Element:
    """A fundamental unit of a document"""

    id: uuid.UUID
    name: str
    metadata: ElementMetadata
    children: list[Union["Element", str]]

    def __init__(self, name: str, metadata: ElementMetadata = ElementMetadata()):
        self.id = uuid.uuid4()
        self.name = name
        self.metadata = metadata
        self.children = []

    def __str__(self, level=0):
        output = "  " * level + f"[{self.name}]"
        output += self._str_children(level=level)
        return output

    def _str_children(self, level=0):
        output = ""
        for child in self.children:
            if isinstance(child, Element):
                output += "\n" + child.__str__(level=level + 1)
            elif isinstance(child, str):
                output += "\n" + ("  " * level) + child
        return output


class LinkElement(Element):
    """An element with a url"""

    url: str

    def __init__(self, *args, url: str):
        super().__init__(*args)
        self.url = url

    def __str__(self, level=0):
        output = "  " * level + f"[{self.name} Link: {self.url}]"
        output += self._str_children(level=level)
        return output
