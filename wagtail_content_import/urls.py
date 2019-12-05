from django.conf.urls import include, url

from .pickers.microsoft import urls as microsoft_urls

app_name = 'wagtailcontentimport'
urlpatterns = [
    url(r'microsoft/', include(microsoft_urls)),
]
