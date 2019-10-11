from django import template
from django.utils.safestring import mark_safe

from wagtail.core import hooks

register = template.Library()


@register.simple_tag(takes_context=True)
def wagtailcontentimport_pickerjs(context):
    pickers = [fn() for fn in hooks.get_hooks('register_content_import_picker')]

    js_snippets = []

    for picker in pickers:
        js_snippets.extend(picker.media.render_js())
        js_snippets.append(picker.render_js_init(context['request']))

    return mark_safe('\n'.join(js_snippets))
