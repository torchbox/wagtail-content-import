import json

from django.conf import settings
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from ...utils import (
    create_page_from_import, is_importing, set_importing,
    update_page_from_import)
from .utils import GooglePicker, parse_document


@hooks.register("before_create_page")
def create_from_google_doc(request, parent_page, page_class):
    if "google-doc" in request.POST and not is_importing(request):
        set_importing(request)
        parsed_doc = parse_document(json.loads(request.POST["google-doc"]))
        return create_page_from_import(request, parent_page, page_class, parsed_doc)


@hooks.register("before_edit_page")
def edit_from_google_doc(request, page):
    if "google-doc" in request.POST and not is_importing(request):
        set_importing(request)
        parsed_doc = parse_document(json.loads(request.POST["google-doc"]))
        return update_page_from_import(request, page, parsed_doc)


@hooks.register("register_content_import_picker")
def register_content_import_picker():
    client_config = getattr(
        settings, "WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG", ""
    )
    api_key = getattr(settings, "WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY", "")
    if client_config and api_key:
        return GooglePicker(client_config, api_key,)
