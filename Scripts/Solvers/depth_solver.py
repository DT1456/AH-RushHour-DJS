from game import Game
import sys

# set recusion limit
sys.setrecursionlimit(10000)


class Stack:

    def __init__(self) -> None:
        """Initialise empty stack"""
        self._data: list[tuple[str, ...]] = []

    def push(self, element: tuple[str, ...]) -> None:
        """Add element to back of stack"""
        self._data.append(element)

    def pop(self) -> tuple[str, ...]:
        """Remove and return element from back of stack"""
        assert self.size() > 0
        return self._data.pop()

    def size(self) -> int:
        """Find and return size of stack"""
        return len(self._data)


class Solver:

    def __init__(self) -> None:
        """Initialising parent states dict, queue and original board"""

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

    def solve(self, game: Game) -> Game:
        """Searching for solution of the game"""

        self.stack.push(game.tuple_form())
        self.visited = set()
        self.parents = {game.tuple_form(): ()}
        self.original_board = game.tuple_form()

        while self.stack.size() > 0:
            # Remove first item from stack
            current_state = self.stack.pop()

            # Move to current state
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

            # When game is won, save  winning steps
            if game.is_won():
                game.set_moves(self.get_best_path(game))
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

    def get_best_path(self, game: Game) -> list[tuple[str, int]]:
        """Construct the best path based on parents, if game is won"""

        # If game is not won, exit
        if not game.is_won():
            raise Exception('Game not yet won, unable to get best path!')

        # Define game_tuple as current game state
        game_tuple = game.tuple_form()

        # Initialise the list of moves
        moves_list = []
        while self.parents[game_tuple] != ():
            # Set changed_places as list of places that
            # were changed with the move
            changed_places = []

            # Go over the tuples to find differences
            for i in range(len(game_tuple)):
                if game_tuple[i] != self.parents[game_tuple][i]:
                    changed_places.append(i)

                    # Get the car_name
                    if game_tuple[i] == '_':
                        car_name = self.parents[game_tuple][i]
                    else:
                        car_name = game_tuple[i]

            # Based on changed_places, deduce the move that took place
            car_length = game.cars[car_name].get_length()
            if changed_places[1] - changed_places[0] == car_length:
                # Car direction: right
                moves_list.append((car_name, 1))
            elif changed_places[0] - changed_places[1] == car_length:
                # Car direction: left
                moves_list.append((car_name, -1))
            elif changed_places[1] - changed_places[0]\
                    == game.dimension * car_length:
                # Car direction: up
                moves_list.append((car_name, 1))
            elif changed_places[0] - changed_places[1]\
                    == game.dimension * car_length:
                # Car direction: down
                moves_list.append((car_name, -1))
            else:
                raise Exception('Unobtainable move, something went wrong!')
            game_tuple = self.parents[game_tuple]

        # Reverse the list of moves
        moves_list.reverse()

        return moves_list
