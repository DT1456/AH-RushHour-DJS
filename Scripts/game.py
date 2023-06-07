from car import Car
from pathlib import Path


class Game:

    def __init__(self, file_name: str, dimension: int) -> None:
        """Initialises game using file_name and dimension"""
        # Initialise cars and board as dictionaries, set dimension
        self.cars: dict[str, Car] = {}
        self.board: dict[tuple[int, int], str] = {}
        self.dimension = dimension

        # Load cars and board
        self.load_cars(file_name)
        self.load_board()

    def load_board(self) -> None:
        """Loads the board using dimension and the dictionary cars"""
        # Fill the empty board
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.board[(i + 1, j + 1)] = '_'

        # Go over cars and fill in values on the board
        for car_name, car in zip(self.cars, self.cars.values()):
            if car.get_orientation() == 'H':
                for k in range(car.get_length()):
                    self.board[(car.get_row(), car.get_col() + k)] = car_name
            else:
                for k in range(car.get_length()):
                    self.board[(car.get_row() + k, car.get_col())] = car_name

    def load_cars(self, file_name: str) -> None:
        """Loads the cars from file_name"""
        with open(file_name) as f:
            f.readline()

            while True:
                line = f.readline().strip('\n')
                if line == '':
                    break
                car, orientation, col, row, length = line.split(',')
                self.cars[car] = Car(orientation, int(col), int(row), int(length))

    def is_won(self) -> bool:
        """Returns whether the game is won

        If car 'X' can be moved off the board, game is won
        """
        return self.cars['X'].get_col() == self.dimension - 1

    def is_valid_move(self, car_name: str, direction: str) -> bool:
        # check if direction correct
        if self.cars[car_name].orientation == 'H':
            if direction not in ['L', 'R']:
                return False
        else:
            if direction not in ['U', 'D']:
                return False
        # check if empty space (dus ook dimensie bord)
        try:
            car = self.cars[car_name]
            if direction == 'U':
                location_x = car.get_row() - 1
                location_y = car.get_col()
            elif direction == 'D':
                location_x = car.get_row() + car.get_length()
                location_y = car.get_col()
            elif direction == 'L':
                location_x = car.get_row()
                location_y = car.get_col() - 1
            elif direction == 'R':
                location_x = car.get_row()
                location_y = car.get_col() + car.get_length()
            else:
                return False
            if self.board[(location_x, location_y)] != '_':
                return False
        except KeyError:
            return False
        return True

    def move(self, car_name: str, direction: str) -> bool:
        direction = direction.upper()
        if self.is_valid_move(car_name, direction):
            # adjust empty space (eentje erbij, eentje eraf)
            car = self.cars[car_name]
            if direction == 'U':
                location_x = car.get_row() - 1
                location_y = car.get_col()
                self.board[(location_x, location_y)] = car_name
                self.board[(location_x + car.get_length(), location_y)] = '_'
            elif direction == 'D':
                location_x = car.get_row() + car.get_length()
                location_y = car.get_col()
                self.board[(location_x, location_y)] = car_name
                self.board[(car.get_row(), location_y)] = '_'
            elif direction == 'L':
                location_x = car.get_row()
                location_y = car.get_col() - 1
                self.board[(location_x, location_y)] = car_name
                self.board[(location_x, location_y + car.get_length())] = '_'
            else:
                location_x = car.get_row()
                location_y = car.get_col() + car.get_length()
                self.board[(location_x, location_y)] = car_name
                self.board[(location_x, car.get_col())] = '_'

            # adjust car.col of car.row
            car.add_to_row((direction == 'D') - (direction == 'U'))
            car.add_to_col((direction == 'R') - (direction == 'L'))
            return True
        return False

    def __str__(self) -> str:
        board_string = ''
        for i in range(self.dimension):
            for j in range(self.dimension):
                board_string += ' ' + self.board[(i + 1, j + 1)] + ' '
            board_string += '\n\n'
        return board_string


if __name__ == '__main__':

    dimension = int(input('With which board dimension would you like to play'
        ' (6, 9, or 12)?\n'))

    if dimension == 6:
        game_number = input('Which game do you want to play (1, 2 or 3)?\n')
    if dimension == 9:
        game_number = input('Which game do you want to play (4, 5 or 6)?\n')
    if dimension == 12:
        game_number = 7

    path = str(Path(__file__).parent.parent) + f'/Input/Rushhour{dimension}x{dimension}_{game_number}.csv'
    print(path)
    g = Game(path, dimension)

    print(g)
    while not g.is_won():
        try:
            car_name, direction = input('What car to move? Carname and direction split by space!\n').split()
            car_name = car_name.upper()
            if g.move(car_name, direction):
                print(g)
            else:
                print('Invalid command!\n')
        except ValueError:
            print('Invalid command!\n')
