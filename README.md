![Wagtail Content Import](docs/img/wagtail_content_import_logo_with_text.svg)

Wagtail Content Import is a module for importing page content into Wagtail from third-party sources.
Page content is imported into a StreamField, using a set of customisable mappings.
Currently supports:

### As sources:
- Google Docs
- OneDrive/SharePoint

### As files:
- Google Docs documents with:
    - Rich text
    - Tables
    - Images
    - Headings
- Docx files with:
    - Text with bold and italics
    - Headings

### Requirements:
* Django >= 4.2
* Wagtail >= 5.2

For the full documentation, see: https://torchbox.github.io/wagtail-content-import/

### Note for Google Import

If using Google Docs import, for users to authenticate with Google they must either allow third party cookies or add `accounts.google.com` to their allowed domains ([Settings/Privacy and Security/Cookies and other site data in Chrome](chrome://settings/cookies) or [Preferences/Privacy & Security in Firefox](about:preferences#privacy)).