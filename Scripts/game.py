from car import Car
import csv
import os
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random as random
from sys import argv
from typing import Union


class Game:

    def __init__(self, file_name: str, dimension: int) -> None:
        """Initialises game using file_name and dimension"""

        # Initialise cars and board as dictionaries, set dimension and moves
        self.cars: dict[str, Car] = {}
        self.board: dict[tuple[int, int], str] = {}
        self.dimension: int = dimension
        self.moves: list[list[Union[int, str]]] = []

        # Load cars and board
        self.load_cars(file_name)
        self.load_board()

        # Set print option
        self.terminology_print: bool = False
        self.imgcat_print: bool = False

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
            # Skip header
            f.readline()

            # Read in cars, line by line
            while True:
                # Read in line
                line = f.readline().strip('\n')

                # If EOF, break
                if line == '':
                    break

                # Set car_name, orientation, col, row and length
                car_name, orientation, col, row, length = line.split(',')

                # Load in car
                self.cars[car_name] = Car(car_name, orientation, int(col), int(row),
                                          int(length))

    def is_won(self) -> bool:
        """Returns whether the game is won

        If car 'X' can be moved off the board, game is won
        """
        return self.cars['X'].get_col() == self.dimension - 1

    def is_valid_move(self, car_name: str, direction: str) -> bool:
        """Checks and returns whether a certain move is valid"""

        # Check if direction correct
        if self.cars[car_name].get_orientation() == 'H':
            if direction not in ['L', 'R']:
                return False
        else:
            if direction not in ['U', 'D']:
                return False

        # Check if empty space is available
        return self.board_location_is_empty(car_name, direction)

    def board_location_is_empty(self, car_name: str, direction: str) -> bool:
        """Returns whether board location to move to is empty"""

        # Check if direciton is feasible
        if direction not in ['L', 'R', 'U', 'D']:
            return False

        # Get location coordinates for direction to move to
        location_x, location_y = self.get_location(car_name, direction)

        # Return whether board location is empty, catching KeyErrors
        try:
            return self.board[(location_x, location_y)] == '_'
        except KeyError:
            return False

    def get_location(self, car_name: str, direction: str) -> list[int]:
        """Get location to which the car is moving"""

        # Set car
        car = self.cars[car_name]

        # Use direction to get correct location to move to
        if direction == 'U':
            location_x = car.get_row() - 1
            location_y = car.get_col()
        elif direction == 'D':
            location_x = car.get_row() + car.get_length()
            location_y = car.get_col()
        elif direction == 'L':
            location_x = car.get_row()
            location_y = car.get_col() - 1
        else:
            location_x = car.get_row()
            location_y = car.get_col() + car.get_length()

        # Return x, y coordinates
        return [location_x, location_y]

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

            # Store move and direction
            self.moves.append([car_name, self.direction_to_int(direction)])

            return True
        return False

    def direction_to_int(self, direction: str) -> int:
        if direction in ['L', 'U']:
            return -1
        return 1

    def __str__(self) -> str:
        board_string = ''
        for i in range(self.dimension):
            for j in range(self.dimension):
                board_string += ' ' + self.board[(i + 1, j + 1)] + ' '
            board_string += '\n\n'
        return board_string

    def show_image(self) -> None:
        """Shows image in terminal (Terminology or Imgcat)"""
        pixel_to_square = 50

        # Set empty image
        game_image = Image.new('RGB', (self.dimension * pixel_to_square,
                                       self.dimension * pixel_to_square))

        # Fill image with empty tiles
        for i in range(self.dimension):
            for j in range(self.dimension):
                game_image.paste(Image.open('BoardImages/empty_tile.jpeg'),
                                 (i * pixel_to_square, j * pixel_to_square))

        # Fill with pictures of cars
        for car_name, car in zip(self.cars, self.cars.values()):
            game_image.paste(Image.open(car.get_image_string()),
                             ((car.get_col() - 1) * pixel_to_square,
                              (car.get_row() - 1) * pixel_to_square))

        # Print car names (letters) on cars
        game_image_draw = ImageDraw.Draw(game_image)
        font = ImageFont.truetype('Font/FreeSerif.ttf', size=16)
        for car_name, car in zip(self.cars, self.cars.values()):
            text_offset_x, text_offset_y = car.get_text_offset()
            game_image_draw.text(((car.get_col() - 1) * pixel_to_square +
                                 text_offset_x,
                                 (car.get_row() - 1) * pixel_to_square + text_offset_y),
                                 car.car_name, fill=(0, 0, 0), font=font)

        # Save image
        game_image.save('BoardImages/game.jpeg')

        # Show image in desired terminal (Terminology or Imgcat)
        if self.get_terminology_print():
            os.system('tycat BoardImages/game.jpeg')
        else:
            os.system('$HOME/.iterm2/imgcat BoardImages/game.jpeg')

    def show_image_imgcat(self) -> None:
        pixel_to_square = 50
        game_image = Image.new('RGB', (self.dimension * pixel_to_square,
                                       self.dimension * pixel_to_square))
        for i in range(self.dimension):
            for j in range(self.dimension):
                game_image.paste(Image.open('BoardImages/empty_tile.jpeg'),
                                 (i * pixel_to_square, j * pixel_to_square))

        for car_name, car in zip(self.cars, self.cars.values()):
            game_image.paste(Image.open(car.get_image_string()),
                             ((car.get_col() - 1) * pixel_to_square,
                              (car.get_row() - 1) * pixel_to_square))
        game_image.save('BoardImages/game.jpeg')
        os.system("imgcat BoardImages/game.jpeg")

    def show_board(self) -> None:
        if self.get_terminology_print() or self.get_imgcat_print():
            self.show_image()
        else:
            print(self)

    def set_terminology_print_to_true(self) -> None:
        self.terminology_print = True

    def get_terminology_print(self) -> bool:
        return self.terminology_print

    def set_imgcat_print_to_true(self) -> None:
        self.imgcat_print = True

    def get_imgcat_print(self) -> bool:
        return self.imgcat_print

    def output_to_csv(self) -> None:
        with open('output.csv', 'w', encoding='UTF8', newline='') as f:
            csv_writer = csv.writer(f)
            
            # Header
            csv_writer.writerow(['car', 'move'])
            
            # Moves
            for move in self.moves:
                csv_writer.writerow(move)

    def get_step_count(self) -> int:
        return len(self.moves)

    def get_cars(self) -> dict[str, Car]:
        return self.cars

    def get_moves(self) -> list[list[Union[int, str]]]:
        return self.moves


def ask_user_input() -> Game:
    # Ask user for dimension of game
    dimension = int(input('With which board dimension would you like to play'
                    ' (6, 9, or 12)?\n'))

    # Based on dimension, ask user for game to play
    if dimension == 6:
        game_number = int(input('Which game do you want to play (1, 2 or 3)?\n'
                                ))
    if dimension == 9:
        game_number = int(input('Which game do you want to play (4, 5 or 6)?\n'
                                ))
    if dimension == 12:
        game_number = 7

    # Set path
    path = str(Path(__file__).parent.parent) + '/Input/'
    full_name = path + f'Rushhour{dimension}x{dimension}_{game_number}.csv'

    # Return game
    return Game(full_name, dimension)


def use_command_line_input_for_file(argv: list[str]) -> Game:
    """Use CLI to specify the game to play"""

    # Set file_name, path and full file_name
    file_name = argv[2]
    path = str(Path(__file__).parent.parent) + '/Input/'
    full_name = path + file_name

    # Find dimension from file_name
    dimension = int(file_name[file_name.find('x') + 1: file_name.find('_')])

    # Return game
    return Game(full_name, dimension)


def get_help() -> str:
    """Return the help string for the user"""

    # Define help_str and its header
    help_str = 'Welcome to the Rushhour implementation\n'
    help_str += 'Implemented by Duco, Jasmijn and Sabrina\n'
    help_str += '-------------------------------\n\n'
    help_str += 'You have the following options:\n'

    # Add the options
    help_str += '[-h]                            : shows this help menu\n'
    help_str += '[-f RushhourDIMxDIM_GAMENUM.csv]: loads any'\
        ' game (in map Input) via its name\n'
    help_str += 'Adding [-t] at the end            : uses terminology for'\
        ' the board (better visual)\n'
    help_str += 'Adding [-i] at the end            : uses terminology for'\
        ' the board (better visual)\n'
    help_str += 'Else                            : choice menu for the'\
        ' original games\n\n'

    # Show output location
    help_str += 'Output for the game is stored in Output/output.csv\n'

    # Return help_str
    return help_str


if __name__ == '__main__':
    """Run the game in CLI"""

    # Initialise game
    if len(argv) == 2 and argv[1] == '-h':
        print(get_help())
        exit(1)
    elif len(argv) == 3 and argv[1] == '-f':
        game = use_command_line_input_for_file(argv)
    else:
        game = ask_user_input()

        # Ask for terminology print
        if argv[len(argv) - 1] not in ['-i', '-t'] and \
            input('Do you want to print a picture (using Terminology)?'
                  ' (Y/N)\n').upper() == 'Y':
            game.set_terminology_print_to_true()

        # Ask for imgcat print
        if not game.get_terminology_print() and argv[len(argv) - 1] not in ['-i', '-t'] and \
            input('Do you want to print a picture (using Imgcat)?'
                  ' (Y/N)\n').upper() == 'Y':
            game.set_imgcat_print_to_true()

    # Specify print function
    if argv[len(argv) - 1] == '-t':
        game.set_terminology_print_to_true()
    elif argv[len(argv) - 1] == '-i':
        game.set_imgcat_print_to_true()

    # Print game
    game.show_board()

    # While game not won, choose car and direction and move
    while not game.is_won():
        try:
            car_name, direction = input('What car to move? Car name and '
                                        'direction split by space!\n').split()
            car_name = car_name.upper()
            if game.move(car_name, direction):
                game.show_board()
            else:
                print('Invalid command!\n')
        except ValueError:
            print('Invalid command!\n')

    # Moves to output.csv
    game.output_to_csv()
