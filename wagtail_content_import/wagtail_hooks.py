from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.admin.staticfiles import versioned_static
from wagtail.core import hooks


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        versioned_static('wagtail_content_import/css/import-styles.css'),
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_css():
    return format_html(
        '<script src="{}"></script>',
        versioned_static('wagtail_content_import/js/picker.js'),
    )
