from .mappers import get_default_mapper
from django.utils.text import slugify

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
        title = parsed_doc['title']
        mapper_class = cls.mapper_class
        mapper = mapper_class()
        imported_data = mapper.map(parsed_doc['elements'], user=user)
        return cls(
            title=title,
            slug=slugify(title),
            body=imported_data,
            owner=user,
        )