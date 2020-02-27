import json

from django.conf import settings

from wagtail.core import hooks

from .utils import parse_document, GooglePicker
from ...utils import create_page_from_import


@hooks.register("before_create_page")
def create_from_google_doc(request, parent_page, page_class):
    if "google-doc" in request.POST:
        parsed_doc = parse_document(json.loads(request.POST["google-doc"]))
        return create_page_from_import(request, parent_page, page_class, parsed_doc)


@hooks.register('register_content_import_picker')
def register_content_import_picker():
    client_config = getattr(settings, "WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG", "")
    api_key = getattr(settings, "WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY", "")
    if client_config and api_key:
        return GooglePicker(
            client_config,
            api_key,
        )
