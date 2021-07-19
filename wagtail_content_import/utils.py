from django.shortcuts import render

from wagtail.admin.action_menu import PageActionMenu

try:
    from wagtail.admin.views.pages import get_valid_next_url_from_request
except ImportError:
    from wagtail.admin.views.pages.utils import get_valid_next_url_from_request


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


def update_page_from_import(request, page, parsed_doc):
    """
    Renders an edit page with the content of the page replaced with the content in the given document
    """
    page.update_from_import(parsed_doc, request.user)

    edit_handler = page.get_edit_handler()
    edit_handler = edit_handler.bind_to(request=request, instance=page)
    form_class = edit_handler.get_form_class()

    next_url = get_valid_next_url_from_request(request)

    form = form_class(instance=page)
    has_unsaved_changes = True

    edit_handler = edit_handler.bind_to(form=form)

    return render(
        request,
        "wagtailadmin/pages/edit.html",
        {
            "page": page,
            "page_for_status": page,
            "content_type": page.content_type,
            "edit_handler": edit_handler,
            "action_menu": PageActionMenu(
                request, view="edit", page=page, parent_page=page.get_parent()
            ),
            "preview_modes": page.preview_modes,
            "form": form,
            "next": next_url,
            "has_unsaved_changes": has_unsaved_changes,
        },
    )
