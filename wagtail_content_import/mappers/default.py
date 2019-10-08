from uuid import uuid4
from functools import partial

class Mapper:

    def __init__(self, type_to_conversion_function_dict=None):
        if type_to_conversion_function_dict is None:
            self.type_to_conversion_function_dict = {
                'html': partial(self.rename, new_type='paragraph')
            }
        else:
            self.type_to_conversion_function_dict = type_to_conversion_function_dict

    def map(self, intermediate):
        output_streamfield = []
        for element in intermediate:
            try:
                conversion_function = self.type_to_conversion_function_dict[element["type"]]
                converted_element = conversion_function(element)
            except KeyError:
                converted_element = element
            streamfield_element = self.add_streamfield_block_id(converted_element)
            output_streamfield.append(streamfield_element)
        return output_streamfield

    @staticmethod
    def add_streamfield_block_id(block):
        # Add an ID to the block, because wagtail-react-streamfield borks without one
        block['id'] = str(uuid4())
        return block

    @staticmethod
    def rename(element, new_type):
        element['type'] = new_type
        return element
