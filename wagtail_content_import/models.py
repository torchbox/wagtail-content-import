from django.utils.text import slugify

from .mappers import get_default_mapper


class ContentImportMixin:
    """
    Mixin to allow a Page model to import content (currently from Google)
    """

    can_import = True

    mapper_class = get_default_mapper()

    @classmethod
    def create_from_import(cls, parsed_doc, user):
        """
        Factory method to create the Page and populate it from a parsed document.
        """
        page = cls(owner=user)
        page.update_from_import(parsed_doc, user)
        return page

    def update_from_import(self, parsed_doc, user):
        self.title = parsed_doc["title"]
        self.slug = slugify(self.title)
        mapper = self.mapper_class()
        self.body = mapper.map(parsed_doc["elements"], user=user)
