from django.conf import settings
from django.utils.module_loading import import_string

def get_default_mapper_string():
    """
    Get the dotted ``app.Model`` name for the default mapper as a string.
    """
    return getattr(settings, 'WAGTAILCONTENTIMPORT_DEFAULT_MAPPER', 'wagtail_content_import.mappers.streamfield.StreamFieldMapper')


def get_default_mapper():
    """
    Get the default mapper from the ``WAGTAILCONTENTIMPORT_DEFAULT_MAPPER`` setting, defaulting to wagtail_content_import.mappers.streamfield.StreamFieldMapper.
    """
    mapper_string = get_default_mapper_string()

    return import_string(mapper_string)