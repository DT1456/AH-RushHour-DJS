from game import Game
from typing import Optional
import sys

# set recusion depth
sys.setrecursionlimit(10000)


class Stack:

    # Initialise empty stack
    def __init__(self) -> None:
        self._data: list[tuple[str, ...]] = []

    # Add element to back of stack
    def push(self, element: tuple[str, ...]) -> None:
        self._data.append(element)

    # Remove and return element from front of stack
    def pop(self) -> tuple[str, ...]:
        assert self.size() > 0
        return self._data.pop()

    # Find and return size of the stack
    def size(self) -> int:
        return len(self._data)


class Solver:

    def __init__(self) -> None:
        # dict of states previous to current state (key) and current states
        self.parents: dict[tuple[str, ...], tuple[str, ...]]
        self.stack = Stack()
        self.original_board: tuple[str, ...]

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
        """Defining and returning a reversed direction"""
        return -direction

    def get_steps(self, tuple_form: tuple[str, ...]) -> int:
        while self.parents[tuple_form] != ():
            tuple_form = self.parents[tuple_form]
            return self.get_steps(tuple_form) + 1
        return 0

    def solve(self, game: Game) -> Game:
        self.stack.push(game.tuple_form())
        self.visited = set()
        self.parents = {game.tuple_form(): ()}
        self.original_board = game.tuple_form()

        while self.stack.size() > 0:
            # Remove first item from stack
            current_state = self.stack.pop()

            # Move to current state
            game.set_game_via_str(current_state)

            # When game is won, save  winning steps
            if game.is_won():
                game.best_solution_steps = self.get_steps(game.tuple_form())
                return game

            # Mark current state as visited
            self.visited.add(current_state)

            moves_list = self.get_possible_moves(game)

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)

                # Add game.tuple_form() to stack
                if game.tuple_form() not in self.visited:
                    self.stack.push(game.tuple_form())
                    self.visited.add(game.tuple_form())
                    self.parents[game.tuple_form()] = current_state
                # Go back to current state
                game.move(car_name, self.reverse_direction(direction))

        raise Exception('No solution found!\n')

