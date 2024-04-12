from .element import Element, LinkElement, TextElement
from pdfminer.high_level import extract_text

def pdf(pdf_file) -> Element:
  text = extract_text(pdf_file)
  document = TextElement(text=text)
  return document
