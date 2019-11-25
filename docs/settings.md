## General Settings

#### `WAGTAILCONTENTIMPORT_DEFAULT_MAPPER`:

The Mapper class used by default for Page models with ContentImportMixin, unless mapper_class is overridden.
Defaults to StreamFieldMapper.

#### `WAGTAILCONTENTIMPORT_GOOGLE_PARSER`:

The DocumentParser class used for Google Docs. Defaults to `GoogleDocumentParser`.

#### `WAGTAILCONTENTIMPORT_GOOGLE_PARSER`:

The DocumentParser class used for .docx files. Defaults to `DocxParser`.

## Google Picker Settings

#### `GOOGLE_OAUTH_CLIENT_CONFIG` (Required):  

The app's Google client secret. (See: [Google Docs Setup](google_docs_setup.md))

#### `GOOGLE_PICKER_API_KEY` (Required):

The app's Google Picker API key, allowing selection of Google Docs. (See: [Google Docs Setup](google_docs_setup.md))

## Microsoft Picker Settings

#### `MICROSOFT_CLIENT_ID` (Required):  

The app's Microsoft Azure client ID. (See: [Microsoft Setup](microsoft_setup.md))
