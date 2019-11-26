from .base import DocumentParser
from django.utils.html import escape
from .tables import Table, Cell


class GoogleDocumentParser(DocumentParser):
    """Default DocumentParser for Google Docs, taking a JSON Google Doc and converting upon parse() into a list of
    {'type': type, 'value': value} intermediate elements"""
    def __init__(self, document):
        self.document = document

    def elements_to_html(self, paragraph, outer_tag='p'):
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

        for element in paragraph['elements']:
            if 'inlineObjectElement' in element:
                embeds.append(element['inlineObjectElement']['inlineObjectId'])
                continue

            text_run = element.get('textRun')
            if not text_run:
                continue

            content = text_run['content'].strip('\n')
            if not content:
                continue

            prefixes = []
            suffixes = []

            style = text_run['textStyle']
            if style.get('bold'):
                prefixes.append('<b>')
                suffixes.append('</b>')
            if style.get('italic'):
                prefixes.append('<i>')
                suffixes.append('</i>')
            if style.get('link'):
                url = style['link'].get('url')
                # Links without a 'url' field are local bookmark/heading references;
                # skip these as there's no direct equivalent in Wagtail content
                # https://developers.google.com/docs/api/reference/rest/v1/documents#Link
                if url:
                    prefixes.append('<a href="{}">'.format(escape(url)))
                    suffixes.append('</a>')

            html = ''.join(prefixes) + escape(content) + ''.join(suffixes)
            output.append(html)

        if output:
            inner_html = ''.join(output)
            html = f'<{outer_tag}>' + inner_html + f'</{outer_tag}>' if outer_tag else inner_html
        else:
            html = ''
        return {
            'html': html,
            'embeds': embeds,
        }

    def process_embedded_object(self, embed_id):
        embed = self.document['inlineObjects'][embed_id]
        # Currently we only handle images
        image_props = embed['inlineObjectProperties']['embeddedObject'].get('imageProperties')
        if image_props:
            return {
                'type': 'image',
                'value': image_props['contentUri']
            }

    def process_list(self, list_items):
        """
        Return HTML for a series of list items.
        Ordered/unordered lists are only respected at the top level.
        """
        list_id = list_items[0]['list_id']
        list_definition = self.document['lists'][list_id]
        # ordered lists define a glyphType (DECIMAL, ALPHA etc) whereas unordered lists define
        # a constant glyphSymbol
        is_ordered = 'glyphType' in list_definition['listProperties']['nestingLevels'][0]
        list_tag = 'ol' if is_ordered else 'ul'

        # Construct an annotated list that can be efficiently converted into a nested tree
        parts = []
        previous_level = None
        info = {}
        for item in list_items:
            # Update previous info item
            if previous_level is None or previous_level < item['level']:
                info['has_children'] = True

            if previous_level is not None and previous_level > item['level']:
                info['num_to_close'] = previous_level - item['level']

            info = {'html': item['html']}
            previous_level = item['level']
            parts.append(info)

        if previous_level is not None:
            # close last leaf
            info['num_to_close'] = previous_level

        # Generated nested tree
        html = f'<{list_tag}>'
        for part in parts:
            html += '<li>' + part['html']
            html += f'<{list_tag}>' if part.get('has_children') else '</li>'
            for i in range(0, part.get('num_to_close', 0)):
                html += f'</{list_tag}></li>'
        html += f'</{list_tag}>'
        return html

    def process_table(self, table):
        imported_rows = [[Cell(self.get_cell_text(cell)) for cell in row['tableCells']] for row in table['tableRows']]
        return Table(imported_rows)

    @staticmethod
    def get_cell_text(cell):
        """
        Get table cell text
        """
        text = ''
        for content_element in cell['content']:
            if 'paragraph' not in content_element:
                continue
            for paragraph_element in content_element['paragraph']['elements']:
                if 'textRun' not in paragraph_element:
                    continue
                text += paragraph_element['textRun']['content']
        return text.strip()

    def parse(self):
        """
        Parse the document and return a set of intermediate {'type': type, 'value': value} blocks that represent it.
        """
        current_block = []
        unprocessed_embeds = []
        blocks = []

        def close_current_block():
            if current_block:
                blocks.append({
                    'type': 'html',
                    'value': ''.join(current_block)
                })
                current_block.clear()
            if unprocessed_embeds:
                for embed_id in unprocessed_embeds:
                    embed = self.process_embedded_object(embed_id)
                    if embed:
                        blocks.append(embed)
                unprocessed_embeds.clear()

        body = self.document['body']

        # List parsing is rather messy because list items are returned as a
        # series of paragaph objects rather than a nested structure.
        current_list = []

        def close_current_list():
            if current_list:
                html = self.process_list(current_list)
                current_block.append(html)
                current_list.clear()

        for part in body['content']:
            # Part can contain one of sectionBreak, table, tableOfContents, paragraph
            # Currently we only process paragraph and table
            if 'table' in part:
                close_current_block()
                close_current_list()
                table = self.process_table(part['table'])
                blocks.append({
                    'type': 'table',
                    'value': table
                })

            if 'paragraph' not in part:
                continue

            paragraph = part['paragraph']
            style = paragraph['paragraphStyle'].get('namedStyleType')
            if style == 'HEADING_1':
                close_current_list()
                close_current_block()
                try:
                    blocks.append({
                        'type': 'heading',
                        'value': paragraph['elements'][0]['textRun']['content'].strip()
                    })
                except KeyError:
                    pass
            elif 'bullet' in paragraph:     # We're in a list
                content = self.elements_to_html(paragraph, outer_tag=None)
                current_list.append({
                    'html': content['html'],
                    'level': paragraph['bullet'].get('nestingLevel', 0),
                    'list_id': paragraph['bullet']['listId'],
                })
                unprocessed_embeds += content['embeds']
            else:
                close_current_list()

                if paragraph['paragraphStyle']['namedStyleType'] == 'HEADING_2':
                    outer_tag = 'h3'
                elif paragraph['paragraphStyle']['namedStyleType'] == 'HEADING_3':
                    outer_tag = 'h4'
                elif paragraph['paragraphStyle']['namedStyleType'] == 'HEADING_4':
                    outer_tag = 'h5'
                elif paragraph['paragraphStyle']['namedStyleType'] == 'HEADING_4':
                    outer_tag = 'h5'
                else:
                    outer_tag = 'p'

                content = self.elements_to_html(paragraph, outer_tag=outer_tag)
                unprocessed_embeds += content['embeds']
                if content['html']:
                    current_block.append(content['html'])

                # If any embeds were encountered since the last paragraph processed
                # (including within headings / list items that aren't processed as
                # standard paragraphs), close this block and start a new one so that
                # the embed block is in the correct place in the text
                if unprocessed_embeds:
                    close_current_block()

        close_current_list()
        close_current_block()
        return {
            'title': self.document['title'],
            'elements': blocks
        }
