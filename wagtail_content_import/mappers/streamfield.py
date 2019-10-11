from .base import BaseMapper
from .utils import to_tuple, image_element_to_tuple


class StreamFieldMapper(BaseMapper):
    """
    On self.map(), converts a parsed document (self.intermediate_stream) composed of a list of {'type': str, 'value': value} element
    dictionaries to a StreamField-compatible list of (block_type_str, block_contents) tuples. By default, the
    block_type_str is set to element['type'] and block_contents to element[value].

    This can be customised by subclassing and populating type_to_conversion_function_dict, where the keys should be element['type'] strings,
    and the values should be functions, taking an element and returning a StreamField-compatible tuple.
    """

    type_to_conversion_function_dict = {
        'image': image_element_to_tuple
    }

    def map(self):
        output_streamfield = []
        for element in self.intermediate_stream:
            conversion_function = self.type_to_conversion_function_dict.get(element["type"], to_tuple)
            converted_element = conversion_function(element)
            output_streamfield.append(converted_element)
        return output_streamfield

