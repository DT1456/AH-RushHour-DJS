import random


class Car:

    def __init__(self, car_name: str, orientation: str, col: int, row: int,
                 length: int):
        """Initializes Car using column, row and length"""
        self.car_name = car_name.upper()
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length
        self.image_string = ''
        self.text_offset_x = 0
        self.text_offset_y = 0
        self.set_image_string()
        self.set_text_offset()

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
        """Returns image_string"""
        return self.image_string

    def set_image_string(self) -> None:
        """Stores image name as string for loading car visualisation"""

        # Either the red car, or a horizontal/vertical car with length 2/3
        if self.car_name == 'X':
            self.image_string = 'BoardImages/RED.jpeg'
        elif self.get_orientation() == 'H' and self.get_length() == 2:
            random_color = random.SystemRandom().choice(['LGL', 'LBR', 'LPR',
                                                         'LYL', 'TUL', 'ORR'])
            self.image_string = 'BoardImages/H2' + random_color + '.jpeg'
        elif self.get_orientation() == 'H' and self.get_length() == 3:
            random_color = random.SystemRandom().choice(['RL', 'GR', 'BR'])
            self.image_string = 'BoardImages/H3' + random_color + '.jpeg'
        elif self.get_orientation() == 'V' and self.get_length() == 2:
            random_color = random.SystemRandom().choice(['LGD', 'LBU', 'LPU',
                                                         'LYD', 'TUD', 'ORU'])
            self.image_string = 'BoardImages/V2' + random_color + '.jpeg'
        else:
            random_color = random.SystemRandom().choice(['RU', 'GU', 'BD'])
            self.image_string = 'BoardImages/V3' + random_color + '.jpeg'

    def set_text_offset(self) -> None:
        """Stores text offset coordinates for naming cars in visualisation"""

        # Set image_orientation
        image_orientation = self.get_image_string()[-6:-5]

        # Based on car_name, length and image orientation, set text offsets
        if self.car_name == 'X':
            self.text_offset_x = 30
            self.text_offset_y = 17
        elif self.get_length() == 2 and image_orientation == 'L':
            self.text_offset_x = 47
            self.text_offset_y = 17
        elif self.get_length() == 2 and image_orientation == 'R':
            self.text_offset_x = 30
            self.text_offset_y = 17
        elif self.get_length() == 2 and image_orientation == 'D':
            self.text_offset_x = 13.5
            self.text_offset_y = 34
        elif self.get_length() == 2 and image_orientation == 'U':
            self.text_offset_x = 13.5
            self.text_offset_y = 50
        elif self.get_length() == 3 and image_orientation == 'L':
            self.text_offset_x = 75
            self.text_offset_y = 17
        elif self.get_length() == 3 and image_orientation == 'R':
            self.text_offset_x = 50
            self.text_offset_y = 17
        elif self.get_length() == 3 and image_orientation == 'D':
            self.text_offset_x = 13.5
            self.text_offset_y = 50
        else:
            self.text_offset_x = 13.5
            self.text_offset_y = 75

    def get_text_offset(self) -> list[int]:
        """Returns text offset coordinates"""
        return self.text_offset_x, self.text_offset_y
