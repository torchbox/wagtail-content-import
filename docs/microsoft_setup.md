# Setting Up OneDrive/SharePoint Integration

Wagtail OneDrive/SharePoint integration relies on Microsoft APIs, which you will first need to enable for your project:

1. Navigate to the [Microsoft Azure app registrations page](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

2. If you don't have a registration for your project, create a new registration now.

3. Either while creating your registration, or by selecting your project and navigating to `Authentication`, add a new `redirect URI`:

    If you have included `wagtail_content_import.urls` as follows:
    
        url(r'ADDITIONAL_URL_PATH/', include(wagtail_content_import_urls))

   
   The redirect URI will be: `https://BASE_URL/ADDITIONAL_URL_PATH/microsoft/auth/`
   (substituting BASE_URL for your site's url, and ADDITIONAL_URL_PATH for the path under which you have included `wagtail_content_import.urls`)

4. Navigate to `Authentication`. Under `Implicit grant`, add `Access tokens` and `ID tokens`, and save.

5. Finally, navigate to `Overview`, and copy the `Application (client) ID` into the `WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID` setting.

Note: you may need to configure your server to set a [Cross-Origin-Opener-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy) of "unsafe-none" for the file picker popup to function correctly. On applications running Django versions >= 4 and using `django.middleware.security.SecurityMiddleware`, this can be done by setting `SECURE_CROSS_ORIGIN_OPENER_POLICY = "unsafe-none"`.
