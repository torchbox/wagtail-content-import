from django.urls import path

from . import views

app_name = 'content_import_google'

urlpatterns = [
    path('oauth/complete/', views.process_google_oauth, name='complete_oauth'),
    path('choose/', views.GoogleDocImportChooserView.as_view(), name='choose'),
    path('search/', views.GoogleDocSearchView.as_view(), name='search'),
]
