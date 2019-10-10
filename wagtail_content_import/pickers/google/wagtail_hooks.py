from django.urls import include

from django.urls import path

from wagtail.core import hooks

from .utils import parse_document, get_oauth_credentials

from . import urls
from ...utils import create_page_from_import


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('content-import-google/', include(urls, namespace='content_import_google')),
    ]

@hooks.register("before_create_page")
def create_from_google_doc(request, parent_page, page_class):
    if "google-doc-id" in request.GET and request.method == "GET":
        parsed_doc = parse_document(
            get_oauth_credentials(request.user), request.GET["google-doc-id"]
        )
        return create_page_from_import(request, parent_page, page_class, parsed_doc)