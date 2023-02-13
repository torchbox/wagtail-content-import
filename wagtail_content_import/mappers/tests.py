import re
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.test import TestCase
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.models import Page
else:
    from wagtail.core.models import Page

from wagtail.images import get_image_model
from wagtail.images.tests.utils import (
    get_test_image_file, get_test_image_file_jpeg)

from ..parsers.tables import Cell, Table
from .converters import (
    ImageConverter, RichTextConverter, TableConverter, TextConverter)

FIND_BLOCK_KEYS = re.compile('( ?data-block-key="[^"]+")')


class TestConverters(TestCase):
    def setUp(self):
        self.page = Page(
            title='test',
            slug='test'
        )
        Page.objects.last().add_child(
            instance=self.page
        )

    def test_text_conversion(self):
        text_converter = TextConverter("test_block")
        test_element = {"type": "html", "value": "test_text"}
        converted_element = text_converter(test_element)
        self.assertEqual(
            converted_element,
            ("test_block", "test_text"),
            "Should be: ('test_block', 'test_text'",
        )

    def test_plain_rich_text_conversion(self):
        text_converter = RichTextConverter("test_block")
        test_element = {"type": "html", "value": "test_text"}
        converted_element = text_converter(test_element)
        self.assertEqual(converted_element[0], "test_block", "Should be: 'test_block'")
        rich_text = converted_element[1].source
        rich_text_without_block_keys = FIND_BLOCK_KEYS.sub("", rich_text)
        self.assertEqual(
            rich_text_without_block_keys, "<p>test_text</p>", "Should be: 'test_text"
        )

    def test_rich_text_script_tags_removed(self):
        text_converter = RichTextConverter("test_block")
        test_element = {"type": "html", "value": "<script>test_text</script>"}
        converted_element = text_converter(test_element)
        self.assertNotIn(
            "script", converted_element[1].source, "Should not contain script tags."
        )

    def test_rich_text_converts_links(self):
        # Test that links exactly matching page urls are converted to internal links
        text_converter = RichTextConverter("test_block")
        exact_link_element = {"type": "html", "value": f'<p><a href="{self.page.get_full_url()}">a link</a></p>'}
        converted_element = text_converter(exact_link_element)
        self.assertEqual(
            f'<p><a linktype="page" id="{self.page.id}">a link</a></p>',
            FIND_BLOCK_KEYS.sub("", converted_element[1].source),
            "Should be converted to page link"
        )
        inexact_url = f'{self.page.get_full_url()}?this=that'
        inexact_link_element = {"type": "html", "value": f'<p><a href="{inexact_url}">a link</a></p>'}
        converted_element = text_converter(inexact_link_element)
        self.assertEqual(
            f'<p><a linktype="external" href="{inexact_url}">a link</a></p>',
            FIND_BLOCK_KEYS.sub("", converted_element[1].source),
            "Should not be converted to page link"
        )

    def test_table_conversion(self):
        table_converter = TableConverter("test_block")
        test_table = Table([[Cell("0"), Cell("1")], [Cell("2"), Cell("3")]])
        test_element = {"type": "table", "value": test_table}
        converted_element = table_converter(test_element)
        self.assertEqual(converted_element[0], "test_block", "Should be 'test_block'")
        self.assertEqual(
            converted_element[1],
            {"data": [["0", "1"], ["2", "3"]]},
            "Should be: {'data': [['0', '1'], ['2', '3']]}",
        )

    def test_image_conversion(self):
        image_converter = ImageConverter("test_block")
        test_image_file = get_test_image_file()
        test_image_file.seek(0)
        image_converter.fetch_image = MagicMock(
            return_value=("content_import_test_image", test_image_file.read())
        )
        test_user = User.objects.create_user(
            username="tester", email="test@test", password="top_secret"
        )
        converted_element = image_converter(
            {"type": "image", "value": "url"}, user=test_user
        )
        Image = get_image_model()
        self.assertEqual(converted_element[0], "test_block", "Should be 'test_block'")
        self.assertIsInstance(converted_element[1], Image)
        self.assertIn(
            converted_element[1],
            Image.objects.filter(title="content_import_test_image"),
        )

    def test_image_conversion_with_duplicate(self):
        image_converter = ImageConverter("test_block")
        test_image_file = get_test_image_file()
        test_image_file.seek(0)
        test_image_file_2 = get_test_image_file_jpeg()
        test_image_file_2.seek(0)
        image_converter.fetch_image = MagicMock(
            return_value=("content_import_test_image", test_image_file.read())
        )
        test_user = User.objects.create_superuser(
            username="admin_tester", email="test@test", password="top_secret"
        )

        # Run the image converter once
        _, imported_image = image_converter(
            {"type": "image", "value": "url"}, user=test_user
        )

        # Now try to reimport by running the converter again
        Image = get_image_model()
        converted_element = image_converter(
            {"type": "image", "value": "url"}, user=test_user
        )
        self.assertEqual(converted_element[0], "test_block", "Should be 'test_block'")
        self.assertIsInstance(converted_element[1], Image)

        # Check we reuse the first imported instance, rather than importing a duplicate
        self.assertEqual(
            converted_element[1],
            imported_image
        )

        # Now import a different image by running the converter again
        image_converter.fetch_image = MagicMock(
            return_value=("content_import_test_image", test_image_file_2.read())
        )
        new_converted_element = image_converter(
            {"type": "image", "value": "url"}, user=test_user
        )
        self.assertIsInstance(new_converted_element[1], Image)

        # Check we recognise the new image as a non-duplicate, and import it separately
        self.assertNotEqual(
            new_converted_element[1],
            imported_image
        )
