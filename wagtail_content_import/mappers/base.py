class BaseMapper:
    """
    Base mapper to take a parser output (self.intermediate_stream) and map it to the desired input format on self.map()
    """
    def __init__(self, intermediate_stream):
        self.intermediate_stream = intermediate_stream

    def map(self):
        raise NotImplementedError
