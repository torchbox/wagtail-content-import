def to_tuple(element, new_type=None):
    """
    Converts a parser output element {'type': type, 'value': value} into (type, value), changing type to new_type if supplied.
    """
    type = new_type if new_type else element['type']
    return (type, element['value'])
