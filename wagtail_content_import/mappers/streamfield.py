from functools import partial
from .base import BaseMapper
from .utils import to_tuple


class StreamFieldMapper(BaseMapper):

    type_to_conversion_function_dict = {
        'html': partial(to_tuple, new_type='paragraph'),
    }

    def map(self):
        output_streamfield = []
        for element in self.intermediate_stream:
            conversion_function = self.type_to_conversion_function_dict.get(element["type"], to_tuple)
            converted_element = conversion_function(element)
            output_streamfield.append(converted_element)
        return output_streamfield

