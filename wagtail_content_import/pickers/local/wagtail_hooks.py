from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from ...utils import (
    create_page_from_import, is_importing, set_importing,
    update_page_from_import)
from .utils import LocalPicker, parse_document


@hooks.register("register_content_import_picker")
def register_content_import_picker():
    return LocalPicker()


@hooks.register("before_create_page")
def create_from_local_doc(request, parent_page, page_class):
    if "local-doc" in request.FILES and not is_importing(request):
        set_importing(request)
        parsed_doc = parse_document(request.FILES["local-doc"].file)
        return create_page_from_import(request, parent_page, page_class, parsed_doc)


@hooks.register("before_edit_page")
def edit_from_local_doc(request, page):
    if "local-doc" in request.FILES and not is_importing(request):
        set_importing(request)
        parsed_doc = parse_document(request.FILES["local-doc"].file)
        return update_page_from_import(request, page, parsed_doc)
