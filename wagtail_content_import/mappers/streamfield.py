from functools import partial
from .base import BaseMapper
from .utils import add_streamfield_block_id, rename


class StreamFieldMapper(BaseMapper):

    type_to_conversion_function_dict = {
        'html': partial(rename, new_type='paragraph')
    }

    def map(self):
        output_streamfield = []
        for element in self.intermediate_stream:
            try:
                conversion_function = self.type_to_conversion_function_dict[element["type"]]
                converted_element = conversion_function(element)
            except KeyError:
                converted_element = element
            streamfield_element = add_streamfield_block_id(converted_element)
            output_streamfield.append(streamfield_element)
        return output_streamfield

