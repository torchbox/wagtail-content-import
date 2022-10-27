from django.urls import include, path
from django.utils.html import format_html
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import hooks
else:
    from wagtail.core import hooks

from . import admin_views


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        versioned_static('wagtail_content_import/css/import-styles.css'),
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        versioned_static('wagtail_content_import/js/picker.js'),
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [
        path("confirm-dialog/", admin_views.confirm_dialog, name='confirm_dialog'),
    ]

    return [
        path(
            "content-import/",
            include(
                (urls, "wagtail_content_import_admin"),
                namespace="wagtail_content_import_admin",
            ),
        )
    ]
