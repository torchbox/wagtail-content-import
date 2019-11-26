from django.shortcuts import render
from django.utils.text import slugify

from wagtail.admin.action_menu import PageActionMenu
from wagtail.admin.views.pages import get_valid_next_url_from_request


def create_page_from_import(request, parent_page, page_class, parsed_doc):
    """
    Renders a pre-populated create page based on a parsed document for a Page model with ContentImportMixin
    """

    page = page_class.create_from_import(parsed_doc, request.user)

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
