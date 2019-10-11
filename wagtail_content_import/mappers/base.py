class BaseMapper:
    """
    Base mapper to take a parser output (intermediate_stream) and map it to the desired input format on self.map()
    """
def map(self, intermediate_stream):
        raise NotImplementedError
