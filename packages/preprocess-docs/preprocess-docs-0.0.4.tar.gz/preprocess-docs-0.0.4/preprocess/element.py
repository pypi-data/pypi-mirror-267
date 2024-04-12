class Element:
  def __init__(self, name):
    self.name = name
    self.children = []

  def __str__(self, spaces=0):
    output = "  "*spaces + f'[{self.name}]'
    for child in self.children:
      output += "\n" + child.__str__(spaces=spaces+1)
    return output


class TextElement(Element):
  def __init__(self, text):
    super().__init__("Text")
    self.text = text

  def __str__(self, spaces=0):
    return "  "*spaces + f'[Text: {self.text}]'


class LinkElement(Element):
  def __init__(self, text, url):
    super().__init__("Link")
    self.text = text
    self.url = url

  def __str__(self, spaces=0):
    return "  "*spaces + f'[Text: {self.text}, Link: {self.url}]'
