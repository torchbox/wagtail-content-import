from django.contrib.auth.models import User
from django.test import TestCase

from wagtail.images import get_image_model

from unittest.mock import MagicMock

from .converters import ImageConverter, RichTextConverter, TextConverter, TableConverter
from ..parsers.tables import Table, Cell


class testConverters(TestCase):
    def test_text_conversion(self):
        text_converter = TextConverter('test_block')
        test_element = {'type': 'html', 'value': 'test_text'}
        converted_element = text_converter(test_element)
        self.assertEqual(converted_element, ('test_block', 'test_text'), "Should be: ('test_block', 'test_text'")

    def test_plain_rich_text_conversion(self):
        text_converter = RichTextConverter('test_block')
        test_element = {'type': 'html', 'value': 'test_text'}
        converted_element = text_converter(test_element)
        self.assertEqual(converted_element[0], 'test_block', "Should be: 'test_block'")
        self.assertEqual(converted_element[1].source, 'test_text', "Should be: 'test_text")

    def test_rich_text_script_tags_removed(self):
        text_converter = RichTextConverter('test_block')
        test_element = {'type': 'html', 'value': '<script>test_text</script>'}
        converted_element = text_converter(test_element)
        self.assertNotIn('script', converted_element[1].source, "Should not contain script tags.")

    def test_table_conversion(self):
        table_converter = TableConverter('test_block')
        test_table = Table([[Cell('0'), Cell('1')], [Cell('2'), Cell('3')]])
        test_element = {'type': 'table', 'value': test_table}
        converted_element = table_converter(test_element)
        self.assertEqual(converted_element[0], 'test_block', "Should be 'test_block'")
        self.assertEqual(converted_element[1], {'data': [['0', '1'], ['2', '3']]}, "Should be: {'data': [['0', '1'], ['2', '3']]}")

    def test_image_conversion(self):
        image_converter = ImageConverter('test_block')
        image_converter.fetch_image = MagicMock(return_value=('content_import_test_image', b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV\xca\x00\x00\x00\x03PLTE\x00\x00\x00\xa7z=\xda\x00\x00\x00\x01tRNS\x00@\xe6\xd8f\x00\x00\x00\nIDAT\x08\xd7c`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"))
        #one pixel image from https://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png
        test_user = User.objects.create_user(username='tester', email='test@test', password='top_secret')
        converted_element = image_converter({'type': 'image', 'value': 'url'}, user=test_user)
        Image = get_image_model()
        self.assertEqual(converted_element[0], 'test_block', "Should be 'test_block'")
        self.assertIsInstance(converted_element[1], Image)
        self.assertIn(converted_element[1], Image.objects.filter(title='content_import_test_image'))









