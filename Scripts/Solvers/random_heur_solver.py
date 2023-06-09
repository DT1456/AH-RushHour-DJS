from game import Game
import random as random
import sys


class Solver:

    def __init__(self) -> None:
        """Implements Random Heuristics Solver

        Play moves until the game is won, remember visited states
        Rerun a specific amount of times (repetition_count), only when
        improving
        """

        # Set repetition_count for reiterating the game
        self.repetition_count = 100

        # Store steps taken in this solution
        self.current_solution_steps = 0

        # Best solution step count
        self.best_solution_steps = sys.maxsize

        # Initialises original board, winning strategy and visited states
        self.original_board: tuple[str, ...]
        self.winning_strategy: tuple[str, ...] = ()
        self.visited_states: set[str] = set()

    def re_init(self) -> None:
        """Reinitialises for rerun. Is a sparse form of __init__"""
        self.repetition_count = 100
        self.current_solution_steps = 0
        self.best_solution_steps = sys.maxsize
        self.original_board = ()
        self.winning_strategy = ()

    def solve(self, game: Game) -> Game:
        """Solve the game by repeating solve_once"""

        # Make sure the game is in original state
        self.re_init()

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
        self.visited_states = set()

        # While game not won, keep playing moves and incrementing steps
        while not game.is_won() and steps <= self.best_solution_steps:
            game = self.play_move(game)

            # Print game if print_states is True
            if game.get_print_states():
                game.show_board()
            steps += 1

            # Remove unnecessary move for less storage
            game.moves.pop()

        # Set best solution and return game
        if steps <= self.best_solution_steps and game.is_won():
            game.set_visited_state_count(steps)
            self.best_solution_steps = steps
            self.winning_strategy = game.tuple_form()

        return game

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""

        # If no games visited yet, we are at the original board: add game
        if len(self.visited_states) == 0:
            self.visited_states = set(str(game))

        # Get possible moves
        moves_list = self.get_possible_moves(game)

        # Pick a random car and a random direction
        move = random.choice(moves_list)
        car_name, direction = move
        game.move(car_name, direction)

        # If game is already visited and other moves possible: repick a move
        while str(game) in self.visited_states and len(moves_list) > 1:
            # Remove the move
            moves_list.remove(move)

            # Undo the move
            game.move(car_name, self.reverse_direction(direction))

            # Pick a new move and play it
            move = random.choice(moves_list)
            car_name, direction = move
            game.move(car_name, direction)

        # If length of moves_list is 1, simply play that move:
        #     All adjacent states have already been visited
        if len(moves_list) == 1:
            move = random.choice(moves_list)
            car_name, direction = move
            game.move(car_name, direction)

        # Add new state to visited_states
        self.visited_states.add(str(game))

        # Return game
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

    def reverse_direction(self, direction: int) -> int:
        """Return reversed direction"""
        return -direction
