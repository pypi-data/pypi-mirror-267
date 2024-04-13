from .element import Element
from typing import Optional, Union

from pdfminer.high_level import extract_text

def pdf(pdf_file) -> Optional[Union[Element, str]]:
  text = extract_text(pdf_file)
  return text
