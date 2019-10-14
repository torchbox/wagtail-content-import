from .base import BaseMapper


class StreamFieldMapper(BaseMapper):
    """
    On self.map(), converts a parsed document (self.intermediate_stream) composed of a list of {'type': str, 'value': value} element
    dictionaries to a StreamField-compatible list: typically (block_type_str, block_contents) tuples.
    """

    def map(self, intermediate_stream, **kwargs):
        output_streamfield = []
        for element in intermediate_stream:
            conversion_method = getattr(self, element['type'], None)
            if conversion_method:
                converted_element = conversion_method(element, **kwargs)
                output_streamfield.append(converted_element)
        return output_streamfield
