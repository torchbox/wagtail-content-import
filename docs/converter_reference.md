# Converters

Converters are callable classes, which when called, take elements of the intermediate `{'type': type, 'value': value}` format (and keyword arguments) and
return streamfield-compatible tuples of the `(block_name, block_content)` form. All converters inherit from `wagtail_content_import.mappers.converters.BaseConverter`, and take a `block_name` on init.

## `RichTextConverter(block_name, features=None)`

Produces Draftail-compatible html suitable for a `RichTextBlock`, using either the features listed in `features` or the basic rich text features
registered in the Wagtail feature registry (see [the Wagtail documentation](https://docs.wagtail.io/en/v2.8/advanced_topics/customisation/page_editing_interface.html)).

## `TextConverter(block_name)`

Passes the element's `value` field directly through as the block content. Note that this must be escaped, as no whitelisting takes place.

## `ImageConverter(block_name)`

Imports an image found at the url given by the element's `value`, setting the title to the element's `title` if given, and the owner to the `user` kwarg if
provided on calling, and returns the image as the block content.

## `TableConverter(block_name)

Produces a text table from the intermediate table representation, compatible with `wagtail.contrib.table_block.blocks.TableBlock`.
