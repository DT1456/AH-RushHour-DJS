from game import Game
import random as random
import sys


class Solver:

    def __init__(self) -> None:
        """Initialise hil climber by setting repetition count"""
        self.repetition_count = 100
        self.current_solution_steps = 0
        self.best_solution_steps = sys.maxsize
        self.original_board: tuple[str, ...] = ()
        self.winning_strategy: tuple[str, ...] ()

    def solve(self, game: Game) -> Game:
        """Solve the game by repeating solve_once"""

        # Set the original board
        self.original_board = game.tuple_form()

        for _ in range(self.repetition_count):
            # Go back to the original board
            game.set_game_via_str(self.original_board)

            # Solve the game once
            game = self.solve_once(game)
            
        # Make sure the game is in winning state if it exists
        if self.winning_strategy != ():
            game.set_game_via_str(self.winning_strategy)
        return game

    def solve_once(self, game: Game) -> Game:
        """Solve the game iteratively by playing random moves"""

        # For step count, initialise steps at 0
        steps = 0

        # While game not won, keep playing moves and incrementing steps
        while not game.is_won() and steps <= self.best_solution_steps:
            game = self.play_move(game)
            steps += 1

        if game.is_won():
            self.winning_strategy = game.tuple_form()

        # Set best solution and return game
        if steps <= self.best_solution_steps:
            #print(steps, self.best_solution_steps)
            self.best_solution_steps = steps
            game.set_best_solution_steps(steps)

        return game

    def play_move(self, game: Game) -> Game:
        """Play one random move in order to solve the game"""

        # Get the possible moves
        moves_list = self.get_possible_moves(game)

        # Pick a random car and a random direction from possible moves
        move = random.SystemRandom().choice(moves_list)

        # Play the move
        car_name, direction = move
        game.move(car_name, direction)

        return game

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
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
