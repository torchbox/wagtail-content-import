from django.urls import path

from . import views

app_name = "wagtailcontentimport_microsoft"
urlpatterns = [path("auth/", views.auth, name="auth_view")]
