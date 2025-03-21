import json

from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from ...parsers import get_google_parser
from .. import Picker


def parse_document(document):
    parser = get_google_parser()
    return parser(document).parse()


class GooglePicker(Picker):
    name = "google"
    verbose_name = "Google Docs"
    icon = "icon-doc-full-inverse"

    def __init__(self, oauth_client_config, picker_api_key):
        self.oauth_client_config = json.loads(oauth_client_config)
        self.picker_api_key = picker_api_key

    @property
    def app_id(self):
        return self.oauth_client_config["web"]["project_id"]

    @property
    def client_id(self):
        return self.oauth_client_config["web"]["client_id"]

    def get_context(self):
        return {
            "picker": self,
            "app_id": self.app_id,
            "client_id": self.client_id,
            "picker_api_key": self.picker_api_key,
        }

    js_template = "wagtail_content_import/google_picker_js_init.html"

    def render_js_init(self, request):
        return mark_safe(  # noqa: S308
            render_to_string(self.js_template, self.get_context(), request=request)
        )

    class Media:
        css = {}
        js = [
            "wagtail_content_import/google_picker.js",
            format_html(
                '<script async defer src="https://apis.google.com/js/api.js" onload="window.googlepicker_api_loaded = true;"></script>'
            ),
            format_html(
                '<script async defer src="https://accounts.google.com/gsi/client" onload="window.googlepicker_client_loaded = true;"></script>'
            ),
        ]
