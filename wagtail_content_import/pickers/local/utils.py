from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .. import Picker
from ...parsers import get_docx_parser


def parse_document(document):
    parser = get_docx_parser()
    return parser(document).parse()


class LocalPicker(Picker):
    name = "local"
    verbose_name = "Local file"
    icon = "icon-folder-open-inverse"

    def get_context(self):
        return {
            'picker': self,
        }

    js_template = 'wagtail_content_import/local_picker_js_init.html'

    def render_js_init(self, request):
        return mark_safe(render_to_string(self.js_template, self.get_context(), request=request))

    class Media:
        css = {}
        js = []


