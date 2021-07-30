To change how the document's data is imported to the Page model - for example, importing to a StreamField other than `body`,
you'll need to override the `update_from_import` method. On the `ContentImportMixin`, these are defined as:

```python
from django.utils.text import slugify

class ContentImportMixin:
    # ...

    # Called whenever a page is created or updated from an import
    # (note, when creating, self would be unsaved)
    def update_from_import(self, parsed_doc, user):
        self.title = parsed_doc["title"]
        self.slug = slugify(self.title)

        mapper = self.mapper_class()
        self.body = mapper.map(parsed_doc["elements"], user=user)
```

To import into a different field, replace `body` with the name of your custom field.
