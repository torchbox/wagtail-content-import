from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.module_loading import import_string

def get_google_parser_string():
    """
    Get the dotted ``app.Model`` name for the Google Docs parser as a string.
    """
    return getattr(settings, 'WAGTAILCONTENTIMPORT_GOOGLE_PARSER', 'wagtail_content_import.parsers.google.GoogleDocumentParser')


def get_google_parser():
    """
    Get the Google Docs parserfrom the ``WAGTAILCONTENTIMPORT_GOOGLE_PARSER`` setting, defaulting to wagtail_content_import.parsers.google.GoogleDocumentParser.
    """
    parser_string = get_google_parser_string()

    return import_string(parser_string)