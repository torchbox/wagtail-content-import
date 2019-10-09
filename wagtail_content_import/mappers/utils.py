from uuid import uuid4


def add_streamfield_block_id(block):
    # Add an ID to the block, because wagtail-react-streamfield borks without one
    block['id'] = str(uuid4())
    return block



def rename(element, new_type):
    element['type'] = new_type
    return element
