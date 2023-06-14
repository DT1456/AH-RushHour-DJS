from game import Game
import os
import random.SystemRandom as random_pick


class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = ['L', 'R', 'U', 'D']
        if os.path.exists('output.csv'):
            os.remove('output.csv')

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        # If amount of steps is too big already, break and solve the game
        output_moves = []

        if os.path.exists('output.csv'):
            with open('output.csv') as f:
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
                    output_moves += [line.split(',')]

        if os.path.exists('output.csv') and \
                game.get_step_count() > len(output_moves):
            moves_reversed = game.get_moves()[::-1]
            for i in range(len(moves_reversed)):
                moves_reversed[i][1] = -moves_reversed[i][1]
            store_moves = []

            # Reverse all moves and use output to solve
            for move in moves_reversed + output_moves:
                car_name, move_int = move
                move_int = int(move_int)
                if game.get_cars()[car_name].get_orientation() == 'H':
                    direction = 'R' if move_int == 1 else 'L'
                else:
                    direction = 'D' if move_int == 1 else 'U'
                game.move(car_name, direction)
                store_moves += [[car_name, direction]]
        else:
            while True:
                # Pick a random car and a random direction
                car_name = random_pick().choice(list(game.get_cars()))
                direction = random_pick().choice(self.possible_directions)

                # If the chosen car and direction represent a valid move, move
                if game.move(car_name, direction):
                    break

        return game
