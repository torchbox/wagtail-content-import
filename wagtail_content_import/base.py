class DocumentParser:

    def parse(self):
        raise NotImplementedError


class StreamElement:

    TYPE_HEADING = 'heading'
    TYPE_HTML = 'html'
    TYPE_IMAGE = 'image'
    TYPES = [
        TYPE_HEADING,
        TYPE_HTML,
        TYPE_IMAGE,
    ]

    def __init__(self, element_type, value):
        if not element_type in self.TYPES:
            raise ValueError('Invalid element type')

        self.element_type = element_type
        self.value = value
