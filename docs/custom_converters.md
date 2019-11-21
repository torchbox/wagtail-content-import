Converters are callable classes which convert `{type: type, 'value': value}` elements 
in a parsed document to StreamField blocks. You can write your own custom converters to include
functionality not in the core app: for example, [working with StructBlocks](structblocks.md).

Converters should inherit from `wagtail_content_import.mappers.converters.BaseConverter`, which
provides an `__init__` method which populates `self.block_name`, the field name of the StreamField
block the converter is creating.
 
Converters should implement a `__call__(self, element, **kwargs)` method which returns a 
StreamField-compatible tuple of `(self.block_name, content)` for an `element` of the form `{type: type, 'value': value}`

For example, the default TextConverter is implemented simply as:

```python
from wagtail_content_import.parsers.converters import BaseConverter

class TextConverter(BaseConverter):
    def __call__(self, element, **kwargs):
        return (self.block_name, element['value'])
```

To see how to use a custom converter to map into a StructBlock, see [working with StructBlocks](structblocks.md).
