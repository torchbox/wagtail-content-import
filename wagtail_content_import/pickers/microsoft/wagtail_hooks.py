from io import BytesIO

import requests
from django.conf import settings
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from ...utils import (
    create_page_from_import,
    is_importing,
    set_importing,
    update_page_from_import,
)
from .utils import MicrosoftPicker, parse_document


@hooks.register("register_content_import_picker")
def register_content_import_picker():
    client_id = getattr(settings, "WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID", "")
    if client_id:
        return MicrosoftPicker(client_id)


@hooks.register("before_create_page")
def create_from_microsoft_doc(request, parent_page, page_class):
    if "microsoft-doc" in request.POST and not is_importing(request):
        set_importing(request)
        document_url = request.POST["microsoft-doc"]
        response = requests.get(document_url)
        if response.status_code == 200:
            parsed_doc = parse_document(BytesIO(response.content))
            return create_page_from_import(request, parent_page, page_class, parsed_doc)


@hooks.register("before_edit_page")
def edit_from_microsoft_doc(request, page):
    if "microsoft-doc" in request.POST and not is_importing(request):
        set_importing(request)
        document_url = request.POST["microsoft-doc"]
        response = requests.get(document_url)
        if response.status_code == 200:
            parsed_doc = parse_document(BytesIO(response.content))
            return update_page_from_import(request, page, parsed_doc)
