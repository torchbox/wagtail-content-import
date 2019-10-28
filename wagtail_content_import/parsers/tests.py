import json
import os

from django.test import TestCase

from .google import GoogleDocumentParser


class TestGoogleDocumentParser(TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), "test_document.json"), "r") as test_document_file:
            test_document = json.load(test_document_file)
            self.parser = GoogleDocumentParser(test_document)

    def test_plain_paragraph_to_html(self):
        plain_paragraph = self.parser.document['body']['content'][5]['paragraph']
        parsed_paragraph = self.parser.elements_to_html(plain_paragraph, outer_tag='p')
        self.assertEqual(parsed_paragraph['html'], '<p>A plain text paragraph</p>')

    def test_bold_italic_paragraph_to_html(self):
        styled_paragraph = self.parser.document['body']['content'][7]['paragraph']
        parsed_paragraph = self.parser.elements_to_html(styled_paragraph, outer_tag='p')
        self.assertEqual(parsed_paragraph['html'], '<p>A paragraph with <b>bold</b> and <i>italics</i></p>')

    def test_process_table(self):
        table = self.parser.document['body']['content'][10]['table']
        processed_table = self.parser.process_table(table)
        text_table = [[cell.get_text() for cell in row] for row in processed_table.rows]
        self.assertEqual(text_table, [['a', 'b']])

    def test_process_list(self):
        list_items = [{'html': 'A', 'level': 0, 'list_id': 'kix.ekbd3zuridq8'}, {'html': 'B', 'level': 0, 'list_id': 'kix.ekbd3zuridq8'}]
        html = self.parser.process_list(list_items)
        self.assertEqual(html, '<ol><li>A</li><li>B</li></ol>')

    def test_process_image(self):
        embed = self.parser.process_embedded_object('kix.xrypng5vuptx')
        self.assertEqual(embed, {'type': 'image', 'value': 'https://lh5.googleusercontent.com/dmK7P36vTNwm4Q4pdHO5uofPH6hrnAyX5wtMOO-X09VIs9eTefWBWBdvJmUiVfOzc4TsqbDgouCyah-fvzCXbWcm1PvEjRUoxXgdOte1-G23ccLE_-JX0ZU_tbyXqPdQn3Z4uDcJ5PL8ipN9VA'})
