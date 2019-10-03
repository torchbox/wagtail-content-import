from django.urls import include, path

from wagtail.core import hooks

from . import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('content-import-google/', include(urls, namespace='content_import_google'))
    ]
