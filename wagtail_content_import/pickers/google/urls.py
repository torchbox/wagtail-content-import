from django.urls import path

from . import views

app_name = 'content_import_google'

urlpatterns = [
    path('oauth/complete/', views.process_google_oauth, name='complete_oauth'),
    path('choose/<str:app_label>/<str:model_name>/<int:parent_page_id>', views.GoogleDocImportChooserView.as_view(), name='choose'),
    path('search/', views.GoogleDocSearchView.as_view(), name='search'),
]
