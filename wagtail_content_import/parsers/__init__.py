from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

def get_google_parser_string():
    """
    Get the dotted ``app.Model`` name for the Google Docs parser as a string.
    """
    return getattr(settings, 'WAGTAILCONTENTIMPORT_GOOGLE_PARSER', None)


def get_google_parser():
    """
    Get the Google Docs parserfrom the ``WAGTAILCONTENTIMPORT_GOOGLE_PARSER`` setting, defaulting to wagtail_content_import.parsers.google.GoogleDocumentParser.
    """
    from django.apps import apps
    parser_string = get_google_parser_string()
    if not parser_string:
        from .google import GoogleDocumentParser
        return GoogleDocumentParser
    try:
        return apps.get_model(parser_string)
    except ValueError:
        raise ImproperlyConfigured("WAGTAILIMAGES_IMAGE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "WAGTAILIMAGES_IMAGE_MODEL refers to model '%s' that has not been installed" % parser_string
        )