from django.urls import include, path

from .pickers.microsoft import urls as microsoft_urls

app_name = "wagtailcontentimport"
urlpatterns = [
    path("microsoft/", include(microsoft_urls)),
]
