from django.conf import settings
from django.utils.module_loading import import_string


def get_google_parser_string():
    """
    Get the dotted ``app.Model`` name for the Google Docs parser as a string.
    """
    return getattr(
        settings,
        "WAGTAILCONTENTIMPORT_GOOGLE_PARSER",
        "wagtail_content_import.parsers.google.GoogleDocumentParser",
    )


def get_google_parser():
    """
    Get the Google Docs parser from the ``WAGTAILCONTENTIMPORT_GOOGLE_PARSER`` setting, defaulting to wagtail_content_import.parsers.google.GoogleDocumentParser.
    """
    parser_string = get_google_parser_string()

    return import_string(parser_string)


def get_docx_parser_string():
    """
    Get the dotted ``app.Model`` name for the Office Open XML parser as a string.
    """
    return getattr(
        settings,
        "WAGTAILCONTENTIMPORT_DOCX_PARSER",
        "wagtail_content_import.parsers.microsoft.DocxParser",
    )


def get_docx_parser():
    """
    Get the Office Open XML parser  from the ``WAGTAILCONTENTIMPORT_DOCX_PARSER`` setting, defaulting to wagtail_content_import.parsers.microsoft.DocxParser.
    """

    parser_string = get_docx_parser_string()

    return import_string(parser_string)


def get_pdf_parser_string():
    """
    Get the dotted ``app.Model`` name for the pdf parser as a string.
    """
    return getattr(
        settings,
        "WAGTAILCONTENTIMPORT_PDF_PARSER",
        "wagtail_content_import.parsers.pdf.PDFParser",
    )


def get_parser_for_content_type(content_type):
    parser_by_content_type = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': get_docx_parser_string(),
        'application/pdf': get_pdf_parser_string(),
        'application/vnd.google-apps.document': get_google_parser_string()
    }

    return import_string(parser_by_content_type.get(content_type))
