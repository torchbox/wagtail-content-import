from .mappers.streamfield import StreamFieldMapper

class ContentImportMixin:

    can_import = True

    mapper = StreamFieldMapper