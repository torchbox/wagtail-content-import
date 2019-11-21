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
