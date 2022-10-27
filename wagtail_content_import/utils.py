from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView

IS_IMPORTING_ATTRIBUTE = "_is_importing"


def is_importing(request):
    return getattr(request, IS_IMPORTING_ATTRIBUTE, False)


def set_importing(request):
    setattr(request, IS_IMPORTING_ATTRIBUTE, True)


def create_page_from_import(request, parent_page, page_class, parsed_doc):
    """
    Renders a pre-populated create page based on a parsed document for a Page model with ContentImportMixin
    """

    page = page_class.create_from_import(parsed_doc, request.user)

    class CustomCreateView(CreateView):
        def post(self, request):
            self.page = page
            return self.get(request)

    return CustomCreateView.as_view()(request, *page_class._meta.label_lower.split("."), parent_page.pk)


def update_page_from_import(request, page, parsed_doc):
    """
    Renders an edit page with the content of the page replaced with the content in the given document
    """
    page.update_from_import(parsed_doc, request.user)

    class CustomEditView(EditView):
        def post(self, request):
            self.page = page
            return self.get(request)

    return CustomEditView.as_view()(request, page.pk)
