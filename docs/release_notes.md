# Release Notes

## Version 0.4.1 (16/04/2020)
- Fix: include templates for local picker

## Version 0.4.0 (16/04/2020)
- Feature: an additional picker allowing `docx` import from local files is now included. To use it, add `wagtail_content_import.pickers.local` to
  `INSTALLED_APPS` above `wagtail.admin`.

## Version 0.3.3 (04/03/2020)
- Fix: Google documents with nested or multiple text styles are now parsed correctly

## Version 0.3.2 (03/03/2020)

- Update: `GoogleDocumentsParser` parser now parses underline, superscript, subscript, and strikethrough styles. (Note that using nonstandard
  rich text features requires adding them to both the `RichTextConverter` class and the `RichTextField` or block)
- Update: `RichTextConverter` now uses the Draftail `ContentstateConverter` to validate imported content, so correctly accepts features available in 
  Draftail but not Hallo.js
- Update: `GoogleDocumentsParser` now converts heading styles in Google Docs more straightforwardly to html tags. For example, `HEADING_2` maps to `h2` tags.

## Version 0.3.1 (27/02/2020)

- Update: settings for pickers are now prefixed with `WAGTAILCONTENTIMPORT_` for consistency, so the names are 
  now`WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY`, `WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG` and `WAGTAILCONTENTIMPORT_MICROSOFT_CLIENT_ID`. Make sure to change these when updating!

## Version 0.3.0 (26/02/2020)

- Fix: settings for pickers will no longer cause errors in the edit view when unset or set to blank strings - instead, pickers will hide themselves.
- Update: settings for pickers are now prefixed with `WAGTAIL_CONTENT_IMPORT_`, so the names are now `WAGTAIL_CONTENT_IMPORT_GOOGLE_PICKER_API_KEY`,
  `WAGTAIL_CONTENT_IMPORT_GOOGLE_OAUTH_CLIENT_CONFIG` and `WAGTAIL_CONTENT_IMPORT_MICROSOFT_CLIENT_ID`. Make sure to change these when updating!