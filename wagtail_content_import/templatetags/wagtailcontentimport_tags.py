import re
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from wagtail import hooks, VERSION as WAGTAIL_VERSION
from wagtail.admin.action_menu import ActionMenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def wagtailcontentimport_pickerjs(context):
    pickers = [fn() for fn in hooks.get_hooks("register_content_import_picker") if fn()]

    js_snippets = []

    for picker in pickers:
        js_snippets.extend(picker.media.render_js())
        js_snippets.append(picker.render_js_init(context["request"]))

    return mark_safe("\n".join(js_snippets))


class ImportMenuItem(ActionMenuItem):
    template_name = "wagtail_content_import/import_menu_item.html"

    def __init__(self, picker):
        super().__init__()
        self.label = "Import from %s" % picker.verbose_name
        self.icon_name = re.sub(r'^icon-', '', picker.icon)
        self.name = picker.name

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context["show_dialog"] = (parent_context["view"] != "create")
        return context

    def get_url(self, parent_context):
        if parent_context["view"] == "create":
            return reverse("wagtailadmin_pages:add", args=[
                parent_context["content_type"].app_label,
                parent_context["content_type"].model,
                parent_context["parent_page"].id
            ])
        else:
            return reverse("wagtailadmin_pages:edit", args=[parent_context["page"].id])


def get_picker_buttons_context(context, view):
    pickers = [fn() for fn in hooks.get_hooks("register_content_import_picker") if fn()]
    menu_items = [ImportMenuItem(picker) for picker in pickers]
    flat_context = context.flatten()
    flat_context["view"] = view
    rendered_menu_items = [item.render_html(flat_context) for item in menu_items]

    try:
        default_item = rendered_menu_items.pop(0)
    except IndexError:
        default_item = None

    context["show_menu"] = bool(rendered_menu_items)
    context["rendered_menu_items"] = rendered_menu_items
    context["default_menu_item"] = default_item
    return context


if WAGTAIL_VERSION >= (6, 0):
    action_menu_template = "wagtailadmin/pages/action_menu/menu.html"
else:
    action_menu_template = "wagtail_content_import/action_menu_wrapper.html"


@register.inclusion_tag(action_menu_template, takes_context=True)
def wagtailcontentimport_picker_buttons_create(context):
    return get_picker_buttons_context(context, "create")


@register.inclusion_tag(action_menu_template, takes_context=True)
def wagtailcontentimport_picker_buttons_edit(context):
    return get_picker_buttons_context(context, "edit")
