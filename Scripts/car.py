import random


class Car:

    def __init__(self, car_name: str, orientation: str, col: int, row: int, length: int):
        """Initializes Car useing column, row and length"""
        self.car_name = car_name.upper()
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        self.image_string = ''
        self.set_image_string()

    def get_car_name(self) -> str:
        """Returns car name"""
        return self.car_name

    def get_col(self) -> int:
        """Returns column of Car"""
        return self.col

    def get_row(self) -> int:
        """Returns row of Car"""
        return self.row

    def get_length(self) -> int:
        """Returns length of Car"""
        return self.length

    def get_orientation(self) -> str:
        """Returns orientation of Car"""
        return self.orientation

    def set_col(self, col: int) -> None:
        """Changes column of Car"""
        self.col = col

    def set_row(self, row: int) -> None:
        """Changes row of Car"""
        self.row = row

    def add_to_col(self, x: int) -> None:
        """Adds x to self.col"""
        self.col += x

    def add_to_row(self, x: int) -> None:
        """Adds x to self.row"""
        self.row += x

    def get_image_string(self) -> str:
        return self.image_string

    def set_image_string(self) -> None:
        if self.car_name == 'X':
            self.image_string = 'BoardImages/RED.jpeg'
        elif self.get_orientation() == 'H':
            if self.get_length() == 2:
                random_color = random.SystemRandom().choice(['LG', 'LB', 'LP', 'LY', 'TU', 'OR'])
                self.image_string = 'BoardImages/H2' + random_color + '.jpeg'
            else:
                random_color = random.SystemRandom().choice(['R', 'G', 'B'])
                self.image_string = 'BoardImages/H3' + random_color + '.jpeg'
        else:
            if self.get_length() == 2:
                random_color = random.SystemRandom().choice(['LG', 'LB', 'LP', 'LY', 'TU', 'OR'])
                self.image_string = 'BoardImages/V2' + random_color + '.jpeg'
            else:
                random_color = random.SystemRandom().choice(['R', 'G', 'B'])
                self.image_string = 'BoardImages/V3' + random_color + '.jpeg'
