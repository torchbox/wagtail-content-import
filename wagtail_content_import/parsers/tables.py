class Table:

    def __init__(self, rows):
        self.rows = rows


class Cell:
    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text

