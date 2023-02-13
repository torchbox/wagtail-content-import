To convert elements in the parsed document to a StructBlock, you'll need to write a custom converter (see [Writing Custom Converters](custom_converters.md).)

For a StructBlock, the converter output of a `(self.block_name, content)` tuple should provide `content` as a dict. For example, for a StructBlock:

```python
from wagtail.blocks import CharBlock, ChoiceBlock, StructBlock

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

# #A More Complex Example: A Custom ImageBlock

For a custom ImageBlock:

```python
from django.utils.safestring import mark_safe
from wagtail.blocks import BooleanBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):

    show_full_image = BooleanBlock(required=False)
    image = ImageChooserBlock()

    class Meta:
        icon = "image / picture"
        admin_text = mark_safe("<b>Image Block</b>")
        label = "Image Block"
        template = "pages/blocks/image_block.html" 
```

In a StreamField:

```python
from wagtail.blocks import StreamBlock

class BaseBodyStreamBlock(StreamBlock):
    image_block = ImageBlock()
```

We can write a custom converter which borrows some of the functionality of `ImageConverter`:

```python
from wagtail_content_import.mappers.converters import BaseConverter, ImageConverter

class ImageBlockConverter(BaseConverter):
    def __call__(self, element, user, *args, **kwargs):
        image_url = element['value']
        image_name, image_content = ImageConverter.fetch_image(image_url)
        image = ImageConverter.import_as_image_model(image_name, image_content, owner=user)
        return (self.block_name, {'show_full_image': None, 'image': image})
```
