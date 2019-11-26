from django.conf.urls import url

from . import views


app_name = 'wagtailcontentimport_microsoft'
urlpatterns = [
    url(r'auth/', views.auth, name='auth_view')
]
