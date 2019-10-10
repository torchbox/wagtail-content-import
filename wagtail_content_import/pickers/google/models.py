from ...mappers.streamfield import StreamFieldMapper


class GoogleContentImportMixin:

    can_import_from_google = True

    mapper = StreamFieldMapper
