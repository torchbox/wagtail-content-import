from django import template
from django.utils.safestring import mark_safe
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

register = template.Library()


@register.simple_tag(takes_context=True)
def wagtailcontentimport_pickerjs(context):
    pickers = [fn() for fn in hooks.get_hooks("register_content_import_picker") if fn()]

    js_snippets = []

    for picker in pickers:
        js_snippets.extend(picker.media.render_js())
        js_snippets.append(picker.render_js_init(context["request"]))

    return mark_safe("\n".join(js_snippets))


@register.inclusion_tag(
    "wagtail_content_import/picker_buttons_create.html", takes_context=True
)
def wagtailcontentimport_picker_buttons_create(context):
    pickers = [fn() for fn in hooks.get_hooks("register_content_import_picker") if fn()]
    if pickers:
        context["default_picker"] = pickers[0]
        if len(pickers) > 1:
            context["picker_options"] = pickers[1:]
    return context


@register.inclusion_tag(
    "wagtail_content_import/picker_buttons_edit.html", takes_context=True
)
def wagtailcontentimport_picker_buttons_edit(context):
    pickers = [fn() for fn in hooks.get_hooks("register_content_import_picker") if fn()]
    if pickers:
        context["default_picker"] = pickers[0]
        if len(pickers) > 1:
            context["picker_options"] = pickers[1:]
    return context
