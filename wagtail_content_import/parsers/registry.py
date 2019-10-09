from wagtail.utils.apps import get_app_submodules
from .google import GoogleDocumentParser

_searched_for_parsers = False

_parser_registry = {}
_parser_registry_default = {'application/vnd.google-apps.document': GoogleDocumentParser}


class registerParser:

    def __init__(self, mime_type):
        self.mime_type = mime_type

    def __call__(self, cls):

        _parser_registry[self.mime_type] = cls

        return cls


def search_for_parsers():
    global _searched_for_parsers
    if not _searched_for_parsers:
        list(get_app_submodules('parsers'))
        _searched_for_parsers = True


def get_parser(mime_type):
    search_for_parsers()
    if _parser_registry.get(mime_type):
        return _parser_registry.get(mime_type)
    elif _parser_registry_default.get(mime_type):
        return _parser_registry_default.get(mime_type)
    return None



