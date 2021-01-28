import pdfplumber

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .base import DocumentParser


class PDFParser(DocumentParser):
    """Default DocumentParser for pdf taking a BytesIO pdf file and converting upon parse() into a list of
    {'type': type, 'value': value} intermediate elements"""

    def __init__(self, document):
        with pdfplumber.open(document) as pdf:
            self.pdf = pdf

    def generate_simple_tag(self, content, tag):
        return (
            format_html("<{tag}>{content}</{tag}>", tag=tag, content=content)
            if content
            else ""
        )

    def paragraph_to_html(self, paragraph, outer_tag="p"):
        """
        Compile a paragraph into a HTML string.
        Returns a dictionary of the form:
        {
            'type': 'html',
            'value': html
        }
        """

        return {"type": "html", "value": self.generate_simple_tag(paragraph, outer_tag)}

    def parse(self):
        """
        Parse the document and return a set of intermediate {'type': type, 'value': value} blocks that represent it.
        """
        blocks = []
        title = ""

        for page in self.pdf.pages:
            words = page.extract_words(use_text_flow=True)
            current_paragraph = []
            paragraphs = []
            current_bottom = words[0]['bottom']

            for word in words:
                if abs(word['top'] - current_bottom) > abs((word['bottom'] - word['top'])):
                    text = " ".join(current_paragraph)
                    if (not title) and text:
                        title = text
                    paragraphs.append((self.paragraph_to_html(text), current_bottom))
                    current_paragraph = []
                
                current_paragraph.append(word['text'])
                current_bottom = word['bottom']
            text = " ".join(current_paragraph)
            if (not title) and text:
                title = text
            paragraphs.append((self.paragraph_to_html(" ".join(current_paragraph)), current_bottom))
            
            images = [({'type': "image", 'value': image['stream'].rawdata}, image['bottom']) for image in page.images]

            page_blocks = paragraphs + images
            blocks += [block[0] for block in page_blocks]

        return {"title": title, "elements": blocks}
