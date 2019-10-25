# Wagtail Content Import

A module for Wagtail that provides functionality for importing page content from third-party sources.
Currently supports importing Google Docs into a StreamField.

## Getting Started

### Requirements:
* Django 2.2
* Wagtail 2.2
* Python 3

### To install:
 1. Run `python3 pip install wagtail-content-import`.
 2. Add `'wagtail_content_import'` and `'wagtail_content_import.pickers.google'` to `INSTALLED_APPS`.
 
### To set up:
 Wagtail Google Docs integration relies on Google APIs, which you will first need to enable for your project:

1. Navigate to the [Google API Library](https://console.developers.google.com/apis/library). Select a project for your Wagtail site, or create a new one now.

2. Find and enable the [Google Docs](https://console.developers.google.com/apis/library/docs.googleapis.com) and [Google Drive](https://console.developers.google.com/apis/library/drive.googleapis.com) APIs.
    
3. Find and enable the [Google Picker](https://console.developers.google.com/apis/api/picker.googleapis.com) API, and copy its API key to the setting `GOOGLE_PICKER_API_KEY`.

4. Open the [Credentials](https://console.developers.google.com/apis/credentials) page in the API Console.

5. Select `Create credentials`, then `OAuth client ID`

6. If you haven't already configured the consent screen, you will need to configure this now.

    1. Under `Scopes for Google APIs`, click `Add scope`.

    2. Add `../auth/documents.readonly` and `../auth/drive.readonly` scopes.

        Note: adding these sensitive scopes means that you will need to submit your project for verification by Google to
        avoid user caps and warning pages during use.
        
    3. Add your domain to `Authorised domains`.

 7. For `Application type`, choose `Web application`

 8. Under `Authorised JavaScript origins`, add your domain.

 9. On the Credentials page, next to your Client ID, click the download item to download a JSON file of your client
    secret.

 10. Copy the text from this file, and use it to set `GOOGLE_OAUTH_CLIENT_CONFIG`.

## Basic Usage

1. To enable Google Docs import for a Page model, it should inherit from `ContentImportMixin` 
(`wagtail_content_import.models.ContentImportMixin`). By default, content will be imported into into a StreamField called body
(see [Changing Import Fields](#Changing-Import-Fields) for how to change this).

2. You'll then need to create a Mapper, which maps the parsed document into your StreamField blocks. Create a class deriving from `wagtail_content_import.mappers.streamfield.StreamFieldMapper`:

    ```python
   from wagtail_content_import.mappers.converters import ImageConverter, RichTextConverter, TableConverter, TextConverter 
   from wagtail_content_import.mappers.streamfield import StreamFieldMapper
   
    class MyMapper(StreamFieldMapper):
        html = RichTextConverter('my_RichTextBlock_name')
        image = ImageConverter('my_ImageBlock_name')
        heading = TextConverter('my_CharBlock_or_TextBlock_name')
        table = TableConverter('my_TableBlock_name')    
    ```

    The above example assumes use of the simple blocks included with Wagtail. For StructBlocks, see [Working with StructBlocks](#Working-with-StructBlocks).

3. Set mapper_class on your Page model to your new mapper class (or set it as `WAGTAILCONTENTIMPORT_DEFAULT_MAPPER` to use it for all imports by default).

4. You should now see a button near the action menu when creating a new Page of your class in the admin, giving you the option to import a document.

## The Content Import Flow

The Wagtail Content Import app provides:
* **Pickers** - which select and import raw document data 
* **Parsers** - which parse the raw document data into a standard intermediate form
* **Mappers** - which convert this intermediate form into a final output (typically a Wagtail StreamField)

The typical flow is as follows, for a Page model with ContentImportMixin:

1. The Create view in the Wagtail Admin provides a button, which calls a picker.

2. The picker enables a document to be selected, and makes a POST request to the Create view with the document data.

3. The Wagtail hook for "before_create_page" in the picker detects the document, and calls a relevant parser.

4. The parser's parse() method converts the raw document data to a list of {'type': type, 'value': value} elements.

5. The create_page_from_import function is called, which in turn passes the parsed data to the Page model's 
create_from_import method (inherited from ContentImportMixin).

6. By default, this creates an instance of the Page's mapper_class, then uses its map() method to call a relevant
Converter for each {'type': type, 'value': value} element. This returns a StreamField-compatible list of  ('block_name', block_content) tuples.

7. Finally a Page model instance is created (but not saved) with the document's title, and the content inserted into a field called body. 

8. The Create view is then rendered with the Page model instance bound to the form.

## Customising Content Import

### Changing Import Fields

To change how the document's data is imported to the Page model - for example, importing to a StreamField other than `body`,
you'll need to override the `create_from_import` method. On the `ContentImportMixin`, this is defined as:
```python
    from django.utils.text import slugify

    @classmethod
    def create_from_import(cls, parsed_doc, user):
        """
        Factory method to create the Page and populate it from a parsed document.
        """
        title = parsed_doc['title']
        mapper_class = cls.mapper_class
        mapper = mapper_class()
        imported_data = mapper.map(parsed_doc['elements'], user=user)
        return cls(
            title=title,
            slug=slugify(title),
            body=imported_data,
            owner=user,
        )
```

So to import into a different field, simply replace `body` with the name of your custom field.

### Working with StructBlocks

To convert elements in the parsed document to a StructBlock, you'll need to write a custom converter.
Converters should inherit from `wagtail_content_import.mappers.converters.BaseConverter`, and implement 
a `__call__(self, element, **kwargs)` method which returns a StreamField-compatible tuple of
`(self.block_name, content)`.

In the case of a StructBlock, `content` should be in the form of a dict. For example, for a StructBlock:

```python
from wagtail.core.blocks import CharBlock, ChoiceBlock, StructBlock

class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
```

`content` should be:

```python
{
    'heading_text': heading_text,
    'size': size,
}
```

To do this, we could write a converter:

```python
from wagtail_content_import.mappers.converters import BaseConverter

class HeadingBlockConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        return (self.block_name, {'heading_text': element['value'], 'size': 'h2'})
```

## Reference

### Settings

#### `GOOGLE_OAUTH_CLIENT_CONFIG` (Required):  

The app's Google client secret. (See: [Getting Started](#getting-started))

#### `GOOGLE_PICKER_API_KEY` (Required):

The app's Google Picker API key, allowing selection of Google Docs. (See: [Getting Started](#getting-started))

#### `WAGTAILCONTENTIMPORT_DEFAULT_MAPPER`:

The Mapper class used by default for Page models with ContentImportMixin, unless mapper_class is overridden.
Defaults to StreamFieldMapper.

#### `WAGTAILCONTENTIMPORT_GOOGLE_PARSER`:

The DocumentParser class used for Google Docs. Defaults to `GoogleDocumentParser`.
