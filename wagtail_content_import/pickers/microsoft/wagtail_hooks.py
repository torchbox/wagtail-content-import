import requests

from io import BytesIO

from django.conf import settings

from wagtail.core import hooks

from .utils import MicrosoftPicker, parse_document
from ...utils import create_page_from_import


@hooks.register('register_content_import_picker')
def register_content_import_picker():
    client_id = getattr(settings, "WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID", "")
    if client_id:
        return MicrosoftPicker(client_id)


@hooks.register("before_create_page")
def create_from_microsoft_doc(request, parent_page, page_class):
    if "microsoft-doc" in request.POST:
        document_url = request.POST["microsoft-doc"]
        response = requests.get(document_url)
        if response.status_code == 200:
            parsed_doc = parse_document(BytesIO(response.content))
            return create_page_from_import(request, parent_page, page_class, parsed_doc)
