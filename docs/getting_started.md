## Requirements:
* Django 2.2
* Wagtail 2.2

### To set up:
 1. Run `python3 pip install wagtail-content-import`.
 2. Add `'wagtail_content_import'` to `INSTALLED_APPS` above `wagtail.admin`
 3. Add the urls: include `wagtail_import.urls` in your `urlpatterns` in `urls.py`. This could look like:

        from django.urls import include, path
        from wagtail_content_import import urls as wagtail_content_import_urls
        urlpatterns += [
            path('', include(wagtail_content_import_urls)),
            ]
    Note that `wagtail_content_import.urls` must be above `wagtail.urls` in your `urlpatterns`.

 3. Add the relevant pickers:
     - To import from Google Docs, add`'wagtail_content_import.pickers.google'` to `INSTALLED_APPS` above `wagtail.admin`,
  then follow the steps given in [Google Docs Setup](google_docs_setup.md)
     - To import from OneDrive/SharePoint, add`'wagtail_content_import.pickers.microsoft'` to `INSTALLED_APPS` above `wagtail.admin`,
  then follow the steps given in [Microsoft Setup](microsoft_setup.md)
     - To import from local files, add`'wagtail_content_import.pickers.local'` to `INSTALLED_APPS` above `wagtail.admin`,

 4. You're now ready to set up how content will be imported to your Page models: see [Basic Usage](basic_usage.md)
