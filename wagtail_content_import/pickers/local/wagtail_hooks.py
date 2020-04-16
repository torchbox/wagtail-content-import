import requests

from io import BytesIO

from django.conf import settings

from wagtail.core import hooks

from .utils import LocalPicker, parse_document
from ...utils import create_page_from_import


@hooks.register('register_content_import_picker')
def register_content_import_picker():
    return LocalPicker()


@hooks.register("before_create_page")
def create_from_local_doc(request, parent_page, page_class):
    if "local-doc" in request.FILES:
        parsed_doc = parse_document(request.FILES['local-doc'].file)
        return create_page_from_import(request, parent_page, page_class, parsed_doc)
