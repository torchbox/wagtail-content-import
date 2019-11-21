## The Content Import Flow

The Wagtail Content Import app provides:

- **Pickers** - which select and import raw document data 
- **Parsers** - which parse the raw document data into a standard intermediate form
- **Mappers** - which convert this intermediate form into a final output (typically a Wagtail StreamField)

The typical flow is as follows, for a `Page` model with `ContentImportMixin`:

1. The `Create` view in the Wagtail Admin provides a button, which calls a picker.

2. The picker enables a document to be selected, and makes a POST request to the `Create` view with the document data.

3. The Wagtail hook for `"before_create_page"` in the picker detects the document, and calls a relevant parser.

4. The parser's `parse()` method converts the raw document data to a list of `{'type': type, 'value': value}` elements.

5. The `create_page_from_import` function is called, which in turn passes the parsed data to the Page model's 
`create_from_import` method (inherited from `ContentImportMixin`).

6. By default, this creates an instance of the Page's `mapper_class`, then uses its `map()` method to call a relevant
Converter for each `{'type': type, 'value': value}` element. This returns a StreamField-compatible list of  `('block_name', block_content)` tuples.

7. Finally a `Page` model instance is created (but not saved) with the document's title, and the content inserted into a field called `body`. 

8. The `Create` view is then rendered with the `Page` model instance bound to the form.
