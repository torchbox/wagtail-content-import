from .mappers.streamfield import StreamFieldMapper
from django.utils.text import slugify

class ContentImportMixin:

    can_import = True

    mapper_class = StreamFieldMapper

    @classmethod
    def create_from_import(cls, parsed_doc, user):
        title = parsed_doc['title']
        mapper_class = cls.mapper_class
        mapper = mapper_class(parsed_doc['elements'])
        imported_data = mapper.map()
        return cls(
            title=title,
            slug=slugify(title),
            body=imported_data,
            owner=user,
        )