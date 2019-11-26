from wagtail.core.rich_text import RichText

from django.utils.functional import cached_property
from django.core.files.base import ContentFile
from wagtail.images import get_image_model
from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter

import requests


class BaseConverter:
    """Base class for all converters, which take a intermediate-form {'type': type, 'value': value} element
    and return a (self.block_name, content) StreamField-compatible tuple on __call__"""
    def __init__(self, block_name):
        self.block_name = block_name

    def __call__(self, element, **kwargs):
        raise NotImplementedError


class RichTextConverter(BaseConverter):
    def __init__(self, block_name, features=None):
        self.features = features
        super().__init__(block_name)

    @cached_property
    def editor_html_converter(self):
        return EditorHTMLConverter(self.features)

    def __call__(self, element, **kwargs):
        cleaned_html = self.editor_html_converter.to_database_format(element['value'])
        return (self.block_name, RichText(cleaned_html))


class TextConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        return (self.block_name, element['value'])


class ImageConverter(BaseConverter):
    def __call__(self, element, user, **kwargs):
        image_name, image_content = self.fetch_image(element['value'])
        image = self.import_as_image_model(image_name, image_content, owner=user)
        return (self.block_name, image)

    @staticmethod
    def fetch_image(url):
        response = requests.get(url)

        if not response.status_code == 200:
            return

        file_name = url.split("/")[-1]
        return file_name, response.content

    @staticmethod
    def import_as_image_model(name, content, owner):
        Image = get_image_model()
        image = Image(title=name, uploaded_by_user=owner)
        image.file = ContentFile(content, name=name)
        # Set image file size
        image.file_size = image.file.size

        # Set image file hash
        image.file.seek(0)
        image._set_file_hash(image.file.read())
        image.file.seek(0)

        image.save()
        return image


class TableConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        table = element['value']
        text_table = [[cell.get_text() for cell in row] for row in table.rows]
        return (self.block_name, {'data': text_table})
