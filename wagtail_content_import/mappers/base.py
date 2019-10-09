class BaseMapper:
    def __init__(self, intermediate_stream):
        self.intermediate_stream = intermediate_stream

    def map(self):
        raise NotImplementedError
