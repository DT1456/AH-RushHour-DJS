from game import Game
import os
import sys
from typing import Optional

# set recusion limit
sys.setrecursionlimit(10000)


class Solver:

    def __init__(self) -> None:
        """Initialise Breadth-first search by setting an empty queue"""

        self.queue = Queue()
        self.original_board: tuple[str, ...]

    def re_init(self) -> None:
        """Reinitialise queue"""
        self.queue = Queue()

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

    def solve(self, game: Game) -> Game:
        """Searching for solution of the game"""

        # Reinitialise for reruns
        self.re_init()

        # Add current (original) board to queue, parents and original_board
        self.queue.enqueue(game.tuple_form())
        self.parents = Parents()
        self.parents.add(game.tuple_form(), ())
        self.original_board = game.tuple_form()

        while self.queue.is_big_enough() > 0:
            # Remove first item from queue
            current_state = self.queue.dequeue()

            # Move to current state
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

            # Print game if print_states is True
            if game.get_print_states():
                game.show_board()

            # If game is won, quit and set best solution steps for game
            if game.is_won():
                game.set_moves(self.get_best_path(game))
                print('Storage usage (MB): ',
                      int(os.path.getsize('Solvers/Parents')/1000000))

                # Empty Solvers/Parents
                for parent_file in os.scandir('Solvers/Parents'):
                    file_name = parent_file.name
                    if file_name != '.gitkeep':
                        os.unlink(parent_file.path)
                return game

            moves_list = self.get_possible_moves(game)

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)

                # Add game.tuple_form() to queue
                if not self.parents.is_in(game.tuple_form()):
                    self.queue.enqueue(game.tuple_form())
                    self.parents.add(game.tuple_form(), current_state)

                # Go back to current state
                game.move(car_name, self.reverse_direction(direction))

                # Remove unnecessary moves
                game.moves.pop()
                game.moves.pop()
        # If game not returned yet, no solution found: raise Exception
        raise Exception('No solution found!\n')

    def get_best_path(self, game: Game) -> list[tuple[str, Optional[int]]]:
        """Construct the best path based on parents, if game is won"""

        # If game is not won, exit
        if not game.is_won():
            raise Exception('Game not yet won, unable to get best path!')

        # Define game_tuple as current game state
        game_tuple = game.tuple_form()

        # Initialise the list of moves
        moves_list = []
        while self.parents.get(game_tuple) != ():
            # Set changed_places as list of places that
            # were changed with the move
            changed_places = []

            # Go over the tuples to find differences
            sign = None
            for i in range(len(game_tuple)):
                if game_tuple[i] != self.parents.get(game_tuple)[i]:
                    changed_places.append(i)

                    # Set sign of move
                    if sign is None:
                        if game_tuple[i] == '_':
                            sign = 1
                        else:
                            sign = -1

                    # Get the car_name
                    if game_tuple[i] == '_':
                        car_name = self.parents.get(game_tuple)[i]
                    else:
                        car_name = game_tuple[i]

            # Based on changed_places, deduce the move that took place
            car_length = game.cars[car_name].get_length()
            if abs(changed_places[1] - changed_places[0]) == car_length or \
                abs(changed_places[0] - changed_places[1])\
                    == game.get_dimension() * car_length:
                moves_list.append((car_name, sign))
            else:
                raise Exception('Unobtainable move, something went wrong!')
            game_tuple = self.parents.get(game_tuple)

        # Reverse the list of moves and return
        moves_list.reverse()
        return moves_list


class Queue:

    def __init__(self) -> None:
        """Initialising the empty queue"""
        self._data: list[tuple[str, ...]] = []

    def enqueue(self, element: tuple[str, ...]) -> None:
        """Adding element to back of queue"""
        self._data.append(element)

    def dequeue(self) -> tuple[str, ...]:
        """Remove and return element from front of queue"""
        assert self.size() > 0
        return self._data.pop(0)

    def size(self) -> int:
        """Find and return size of queue"""
        return len(self._data)

    def is_big_enough(self) -> bool:
        """Find and return size of queue"""
        return self.size() > 0


class Parents:

    def __init__(self) -> None:
        """Initialise Parents, a read and write implemenation of nodes"""
        pass

    def add(self, child: tuple[str, ...],
            parent: tuple[str, ...]) -> None:
        """Add child and parent to Parents"""

        # Set name
        name = ''
        for k in child:
            name += k + ','

        # Using name, find parents
        with open('Solvers/Parents/' + name, 'w') as f:
            for v in parent:
                f.write(v + ',')
            f.write('\n')

    def get(self, child: tuple[str, ...]) -> tuple[str, ...]:
        """Get parent based on child"""

        # Set name
        name = ''
        for k in child:
            name += k + ','

        # Find parent using name
        with open('Solvers/Parents/' + name, 'r') as f:
            line = f.readline()
        line_list = line.split(',')
        parent = tuple(line_list[:len(line_list)-1])
        return parent

    def is_in(self, child: tuple[str, ...]) -> bool:
        """Check if child is in Parents"""

        # Set name
        name = ''
        for k in child:
            name += k + ','

        # Return if name in Parents (folder)
        return os.path.exists('Solvers/Parents/' + name)
