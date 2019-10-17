class Table:

    def __init__(self, cells):
        self.cells = cells


class Cell:
    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text

