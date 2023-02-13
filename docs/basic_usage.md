# Basic Usage

1. To enable import for a Page model, it should inherit from `ContentImportMixin`
(`wagtail_content_import.models.ContentImportMixin`). By default, content will be imported into into a StreamField called `body`
(see [Changing Import Fields](changing_import_fields.md) for how to change this).

2. You'll then need to create a Mapper, which maps the parsed document into your StreamField blocks. Create a class deriving from `wagtail_content_import.mappers.streamfield.StreamFieldMapper`:

        from wagtail_content_import.mappers.converters import ImageConverter, RichTextConverter, TableConverter, TextConverter
        from wagtail_content_import.mappers.streamfield import StreamFieldMapper

        class MyMapper(StreamFieldMapper):
            html = RichTextConverter('my_paragraph_block')
            image = ImageConverter('my_image_block')
            heading = TextConverter('my_heading_block')
            table = TableConverter('my_table_block')

      This would map to an example StreamField defined as:

        from wagtail.images.blocks import ImageChooserBlock
        from wagtail.blocks import CharBlock, RichTextBlock, StreamBlock
        from wagtail.contrib.table_block.blocks import TableBlock

        class BaseStreamBlock(StreamBlock):
            """
            Define the custom blocks that `StreamField` will utilize
            """
            my_heading_block = CharBlock()
            my_paragraph_block = RichTextBlock()
            my_image_block = ImageChooserBlock()
            my_table_block = TableBlock()

      Note that the converters require the fields rather than the block classes: `'my_heading_block'`, not `CharBlock`.

      The above example assumes use of the simple blocks included with Wagtail. For StructBlocks, see [Working with StructBlocks](structblocks.md).

3. Set `mapper_class` on your Page model to your new mapper class (or set `WAGTAILCONTENTIMPORT_DEFAULT_MAPPER` to your mapper use it for all imports by default).

4. You should now see a button near the action menu when creating a new Page of your class in the admin, giving you the option to import a document.
