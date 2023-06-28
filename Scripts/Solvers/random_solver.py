from game import Game
import random as random


class Solver:

    def __init__(self) -> None:
        """Implements Random Solver: playing random moves until game won"""
        pass

    def solve(self, game: Game) -> Game:
        """Solve the game iteratively by playing random moves"""

        # While game not won, keep playing moves and incrementing steps
        while not game.is_won():
            game = self.play_move(game)

            # Print game if print_states is True
            if game.get_print_states():
                game.show_board()

        return game

    def play_move(self, game: Game) -> Game:
        """Play one random move in order to solve the game"""

        # Get the possible moves
        moves_list = self.get_possible_moves(game)

        # Pick a random car and a random direction from possible moves
        move = random.choice(moves_list)

        # Play the move
        car_name, direction = move
        game.move(car_name, direction)

        return game

    def get_possible_moves(self, game: Game) -> list[tuple[str, int]]:
        """Get list of possible moves in this state"""

        # Initialise moves_list as an empty list of possible moves
        moves_list = []

        # For all cars, try both moves and add them to moves if valid
        for car_name in game.get_cars():
            for direction in [-1, 1]:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))

        # Return the filled list of moves
        return moves_list
