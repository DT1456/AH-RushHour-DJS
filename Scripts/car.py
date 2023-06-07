class Car:

    def __init__(self, orientation: str, col: int, row: int, length: int):
        """Initializes Car useing column, row and length"""
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        
    def get_col(self) -> int:
        """Returns column of Car"""
        return self.col
    
    def get_row(self) -> int:
        """Returns row of Car"""
        return self.row

    def set_col(self, col: int) -> None:
        """Changes column of Car"""
        self.col = col

    def set_row(self, row: int) -> None:
        """Changes row of Car"""
        self.row = row
    