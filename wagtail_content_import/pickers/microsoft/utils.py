import json

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .. import Picker


class MicrosoftPicker(Picker):
    name = "microsoft"
    verbose_name = "OneDrive"
    icon = "icon-folder-open-inverse"

    def get_context(self):
        return {
            'picker': self,
        }

    js_template = 'wagtail_content_import/microsoft_picker_js_init.html'

    def render_js_init(self, request):
        return mark_safe(render_to_string(self.js_template, self.get_context(), request=request))

    class Media:
        css = {}
        js = [
            'https://js.live.net/v7.2/OneDrive.js',
            'wagtail_content_import/microsoft_picker.js',
        ]


