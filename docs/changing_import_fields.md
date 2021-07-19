To change how the document's data is imported to the Page model - for example, importing to a StreamField other than `body`,
you'll need to override the `create_from_import` and `update_from_import` methods. On the `ContentImportMixin`, these are defined as:

```python
from django.utils.text import slugify

class ContentImportMixin:
    # ...

    @classmethod
    def create_from_import(cls, parsed_doc, user):
        """
        Factory method to create the Page and populate it from a parsed document.
        """
        title = parsed_doc["title"]
        mapper = cls.mapper_class()
        imported_data = mapper.map(parsed_doc["elements"], user=user)

        # Return a new page instance
        return cls(
            title=title,
            slug=slugify(title),
            body=imported_data,
            owner=user,
        )


    def update_from_import(self, parsed_doc, user):
        self.title = parsed_doc["title"]
        self.slug = slugify(self.title)
        mapper = self.mapper_class()

        # Update existing fields
        self.body = mapper.map(parsed_doc["elements"], user=user)
```

To import into a different field, replace `body` with the name of your custom field.
