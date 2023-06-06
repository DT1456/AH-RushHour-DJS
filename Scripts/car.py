class Car:

    def __init__(self, orientation: str, col: int, row: int, length: int):
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

    def get_col(self) -> int:
        return self.col