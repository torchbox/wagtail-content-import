# Release Notes

## Version 0.3.0 (26/02/2020)

- Fix: settings for pickers will no longer cause errors in the edit view when unset or set to blank strings - instead, pickers will hide themselves.
- Update: settings for pickers are now prefixed with `WAGTAIL_CONTENT_IMPORT_`, so the names are now `WAGTAIL_CONTENT_IMPORT_GOOGLE_PICKER_API_KEY`,
  `WAGTAIL_CONTENT_IMPORT_GOOGLE_OAUTH_CLIENT_CONFIG` and `WAGTAIL_CONTENT_IMPORT_MICROSOFT_CLIENT_ID`. Make sure to change these when updating!