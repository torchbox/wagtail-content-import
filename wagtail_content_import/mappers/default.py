from functools import partial
from .utils import add_streamfield_block_id, rename

class BaseMapper:
    def __init__(self, intermediate_stream):
        self.intermediate_stream = intermediate_stream

    def map(self):
        raise NotImplementedError


class StreamFieldMapper(BaseMapper):
    def __init__(self, intermediate_stream, type_to_conversion_function_dict=None):
        self.intermediate_stream = intermediate_stream
        if type_to_conversion_function_dict is None:
            self.type_to_conversion_function_dict = {
                'html': partial(rename, new_type='paragraph')
            }
        else:
            self.type_to_conversion_function_dict = type_to_conversion_function_dict

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

