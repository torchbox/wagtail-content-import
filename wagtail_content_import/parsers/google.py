from django.utils.html import escape

from .base import DocumentParser
from .tables import Cell, Table


class GoogleDocumentParser(DocumentParser):
    """Default DocumentParser for Google Docs, taking a JSON Google Doc and converting upon parse() into a list of
    {'type': type, 'value': value} intermediate elements"""

    def __init__(self, document):
        self.document = document
        self.current_block = []
        self.unprocessed_embeds = []
        self.blocks = []
        # List parsing is rather messy because list items are returned as a
        # series of paragaph objects rather than a nested structure.
        self.current_list = []

    def elements_to_html(self, paragraph, outer_tag="p"):
        """
        Compile a paragraph into a HTML string, optionally with semantic markup for styles.
        Returns a dictionary of the form:
        {
            'html': 'HTML content',
            'embeds': '[A list of embedded object IDs that were found in the paragraph]'
        }
        """
        output = []
        embeds = []

        for element in paragraph["elements"]:
            if not element:
                continue

            if "inlineObjectElement" in element:
                embeds.append(element["inlineObjectElement"]["inlineObjectId"])
                continue

            text_run = element.get("textRun")

            if not text_run:
                continue

            content = text_run.get("content", "").strip("\n")
            if not content:
                continue

            style = text_run["textStyle"]

            prefixes, suffixes = self.get_tags_for_style(style)

            suffixes.reverse()
            html = "".join(prefixes) + escape(content) + "".join(suffixes)
            output.append(html)

        inner_html = "".join(output)

        return {
            "html": (
                f"<{outer_tag}>{inner_html}</{outer_tag}>"
                if outer_tag and inner_html
                else inner_html
            ),
            "embeds": embeds,
        }

    def get_tags_for_style(self, style):
        """
        Given a textStyle dictionary, return a pair of lists of prefix and suffix html tags
        """
        prefixes = []
        suffixes = []

        tag_for_style = {
            'bold': 'b',
            'italic': 'i',
            'underline': 'u',
            'strikethrough': 's',
        }
        for style_key, tag in tag_for_style.items():
            if style.get(style_key):
                prefixes.append("<{}>".format(tag))
                suffixes.append("</{}>".format(tag))

        if style.get("baselineOffset") == "SUPERSCRIPT":
            prefixes.append("<sup>")
            suffixes.append("</sup>")
        elif style.get("baselineOffset") == "SUBSCRIPT":
            prefixes.append("<sub>")
            suffixes.append("</sub>")
        if style.get("link"):
            url = style["link"].get("url")
            # Links without a 'url' field are local bookmark/heading references;
            # skip these as there's no direct equivalent in Wagtail content
            # https://developers.google.com/docs/api/reference/rest/v1/documents#Link
            if url:
                prefixes.append('<a href="{}">'.format(escape(url)))
                suffixes.append("</a>")

        return prefixes, suffixes

    def process_embedded_object(self, embed_id):
        embed = self.document["inlineObjects"][embed_id]
        # Currently we only handle images
        image_props = embed["inlineObjectProperties"]["embeddedObject"].get(
            "imageProperties"
        )
        title = embed["inlineObjectProperties"]["embeddedObject"].get("title", "")
        if image_props:
            return {"type": "image", "value": image_props["contentUri"], "title": title}

    def process_list(self, list_items):
        """
        Return HTML for a series of list items.
        Ordered/unordered lists are only respected at the top level.
        """
        list_id = list_items[0]["list_id"]
        list_definition = self.document["lists"][list_id]
        # ordered lists define a glyphType (DECIMAL, ALPHA etc) whereas unordered lists define
        # a constant glyphSymbol
        is_ordered = (
            "glyphType" in list_definition["listProperties"]["nestingLevels"][0]
        )
        list_tag = "ol" if is_ordered else "ul"

        # Construct an annotated list that can be efficiently converted into a nested tree
        parts = []
        previous_level = None
        info = {}
        for item in list_items:
            # Update previous info item
            if previous_level is None or previous_level < item["level"]:
                info["has_children"] = True

            if previous_level is not None and previous_level > item["level"]:
                info["num_to_close"] = previous_level - item["level"]

            info = {"html": item["html"]}
            previous_level = item["level"]
            parts.append(info)

        if previous_level is not None:
            # close last leaf
            info["num_to_close"] = previous_level

        # Generated nested tree
        html = f"<{list_tag}>"
        for part in parts:
            html += "<li>" + part["html"]
            html += f"<{list_tag}>" if part.get("has_children") else "</li>"
            for i in range(0, part.get("num_to_close", 0)):
                html += f"</{list_tag}></li>"
        html += f"</{list_tag}>"
        return html

    def process_table(self, table):
        imported_rows = [
            [Cell(self.get_cell_text(cell)) for cell in row["tableCells"]]
            for row in table["tableRows"]
        ]
        return Table(imported_rows)

    @staticmethod
    def get_cell_text(cell):
        """
        Get table cell text
        """
        text = ""
        for content_element in cell["content"]:
            if "paragraph" not in content_element:
                continue
            for paragraph_element in content_element["paragraph"]["elements"]:
                if "textRun" not in paragraph_element:
                    continue
                text += paragraph_element["textRun"]["content"]
        return text.strip()

    def close_current_block(self):
        if self.current_block:
            self.blocks.append({"type": "html", "value": "".join(self.current_block)})
            self.current_block.clear()
        if self.unprocessed_embeds:
            for embed_id in self.unprocessed_embeds:
                embed = self.process_embedded_object(embed_id)
                if embed:
                    self.blocks.append(embed)
            self.unprocessed_embeds.clear()

    def close_current_list(self):
        if self.current_list:
            html = self.process_list(self.current_list)
            self.current_block.append(html)
            self.current_list.clear()

    def parse(self):
        """
        Parse the document and return a set of intermediate {'type': type, 'value': value} blocks that represent it.
        """

        body = self.document["body"]

        for part in body["content"]:
            # Part can contain one of sectionBreak, table, tableOfContents, paragraph
            # Currently we only process paragraph and table
            if "table" in part:
                self.close_current_block()
                self.close_current_list()
                table = self.process_table(part["table"])
                self.blocks.append({"type": "table", "value": table})

            if "paragraph" not in part:
                continue

            paragraph = part["paragraph"]
            style = paragraph["paragraphStyle"].get("namedStyleType")
            if style == "HEADING_1":
                self.close_current_list()
                self.close_current_block()
                try:
                    self.blocks.append(
                        {
                            "type": "heading",
                            "value": paragraph["elements"][0]["textRun"][
                                "content"
                            ].strip(),
                        }
                    )
                except KeyError:
                    pass
            elif "bullet" in paragraph:  # We're in a list
                content = self.elements_to_html(paragraph, outer_tag=None)
                self.current_list.append(
                    {
                        "html": content["html"],
                        "level": paragraph["bullet"].get("nestingLevel", 0),
                        "list_id": paragraph["bullet"]["listId"],
                    }
                )
                self.unprocessed_embeds += content["embeds"]
            else:
                self.close_current_list()

                tag_for_style = {
                    'HEADING_2': 'h2',
                    'HEADING_3': 'h3',
                    'HEADING_4': 'h4',
                    'HEADING_5': 'h5',
                    'HEADING_6': 'h6',
                }

                outer_tag = tag_for_style.get(style, 'p')

                content = self.elements_to_html(paragraph, outer_tag=outer_tag)
                self.unprocessed_embeds += content["embeds"]
                if content["html"]:
                    self.current_block.append(content["html"])

                # If any embeds were encountered since the last paragraph processed
                # (including within headings / list items that aren't processed as
                # standard paragraphs), close this block and start a new one so that
                # the embed block is in the correct place in the text
                if self.unprocessed_embeds:
                    self.close_current_block()

        self.close_current_list()
        self.close_current_block()
        return {"title": self.document["title"], "elements": self.blocks}
