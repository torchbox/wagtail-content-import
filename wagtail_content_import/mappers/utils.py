from uuid import uuid4


def add_streamfield_block_id(block):
    # Add an ID to the block, because wagtail-react-streamfield borks without one
    block['id'] = str(uuid4())
    return block


def to_tuple(element, new_type=None):
    type = new_type if new_type else element['type']
    return (type, element['value'])
