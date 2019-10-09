from django.urls import include

import json

from django.shortcuts import render
from django.urls import path
from django.utils.text import slugify

from wagtail.admin.action_menu import PageActionMenu
from wagtail.admin.views.pages import get_valid_next_url_from_request
from wagtail.core import hooks

from .utils import parse_document, get_oauth_credentials

from . import urls
from ...mappers.streamfield import StreamFieldMapper


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
        title = parsed_doc['title']
        mapper = StreamFieldMapper(parsed_doc['elements'])
        body = mapper.map()
        page = page_class(
            title=title,
            slug=slugify(title),
            body=json.dumps(body),
            owner=request.user,
        )
        edit_handler = page_class.get_edit_handler()
        edit_handler = edit_handler.bind_to(request=request, instance=page)
        form_class = edit_handler.get_form_class()

        next_url = get_valid_next_url_from_request(request)

        form = form_class(instance=page, parent_page=parent_page)
        has_unsaved_changes = False

        edit_handler = edit_handler.bind_to(form=form)

        return render(
            request,
            "wagtailadmin/pages/create.html",
            {
                "content_type": page.content_type,
                "page_class": page_class,
                "parent_page": parent_page,
                "edit_handler": edit_handler,
                "action_menu": PageActionMenu(
                    request, view="create", parent_page=parent_page
                ),
                "preview_modes": page.preview_modes,
                "form": form,
                "next": next_url,
                "has_unsaved_changes": has_unsaved_changes,
            },
        )
