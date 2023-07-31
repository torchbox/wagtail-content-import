# Release Notes

## Version 0.10.0 (31/7/2023)

- Move to new Google Identity Service authentication to allow new projects to use the package

## Version 0.9.2 (6/4/2023)

- Wagtail 4.2.2 support, fixing a bug that prevented image import due to a change in function signature

## Version 0.9.0 (17/2/2023)

- Wagtail 4.2 support, drop support for versions < 4.1

## Version 0.8.1 (17/2/2023)

- Wagtail 4 support

## Version 0.8.0 (19/5/2022)

- Feature: Wagtail 3.0 and Django 4.0 support
- Feature: Links matching internal pages in rich text are now automatically converted to page links
- Upgrade consideration: Wagtail versions below 2.11 are no longer supported

## Version 0.7.0 (19/4/2022)

- Fix: Importing empty paragraph elements from Google Docs (now included in the serialized format) no longer fails.

## Version 0.6.0 (11/11/2021)

- Feature: Wagtail Content Import now tries to identify if an imported image already exists in your library, and if so, reuses the existing image instead.

## Version 0.5.0 (03/08/2021)

- Feature: The import button has been added to the page editor on existing pages, allowing editors to update them with imported content.

- Upgrade consideration: Picker trigger event

    If you have created a custom picker, you should update the event that it uses to trigger it to open. Previously, pickers listened for the 'click' event on the import button but we have now added a new event called 'openPicker'.

    For example:

        document.addEventListener('DOMContentLoaded', function() {
          document.querySelectorAll('[data-content-import-picker="my_picker"]').forEach(function (element) {
            // ...

            element.addEventListener('click', function() {  // <----- Change this from 'click' to 'openPicker'
              // ...
            });
          });
        });

    See: [Submitting a new backend](submitting_backend.md)

- Upgrade consideration: Customised ``.create_from_import()`` method

    If you have customised the ``.create_from_import()`` method on any page, you should replace this with a customisation of ``.update_from_import()`` instead. This will allow your customisation to work when the page is being updated or created.

    See: [Changing Import Fields](changing_import_fields.md)

## Version 0.4.2 (10/11/2020)
- Fix: Wagtail 2.11 compatibility

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