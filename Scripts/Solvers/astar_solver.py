from game import Game
from queue import PriorityQueue
import sys
from typing import Optional


class Solver:

    def __init__(self, heuristics_choice: str = 'h0') -> None:
        """Initialises A* solver

        Use a PriorityQueue for prioritising the next state
        Store parents and moves in dict(s) for getting the correct solution
        Use an open and closed set for marking states as open and closed
        """

        # Add open set as the queue for visited states
        self.open_set: PriorityQueue[tuple[int, int, tuple[str, ...]]] = \
            PriorityQueue()

        # Add closed set (marking visited states)
        self.closed_set: set[tuple[str, ...]] = set()

        # Store moves cost in a dictionary based on state
        self.moves_cost: dict[tuple[str, ...], int]

        # Check and set heuristics choice for calculating heuristic
        if heuristics_choice not in ['h0', 'h1', 'h2', 'h3', 'h1h2',
                                     'h1h3']:
            raise Exception('Heuristics choice not possible! You chose: ' +
                            heuristics_choice)
        self.heuristics_choice = heuristics_choice

    def re_init(self, heuristics_choice: str = 'h0') -> None:
        """Reinitialises A* solver for repeated use"""
        self.open_set = PriorityQueue()
        self.closed_set = set()
        self.heuristics_choice = heuristics_choice

    def heuristic(self, game: Game) -> int:
        """Runs the actual heuristic(s)"""

        # Return correct heuristic based on self.heuristics_choice
        if self.heuristics_choice == 'h0':
            return self.h0(game)
        elif self.heuristics_choice == 'h1':
            return self.h1(game)
        elif self.heuristics_choice == 'h2':
            return self.h2(game)
        elif self.heuristics_choice == 'h3':
            return self.h3(game)
        elif self.heuristics_choice == 'h1h2':
            return self.h1(game) + self.h2(game)
        return self.h1(game) + self.h3(game)

    def h0(self, game: Game) -> int:
        """Heuristic 0: always returns zero"""
        return 0

    def h1(self, game: Game) -> int:
        """Heuristic 1: returns the distance of red car to exit"""
        return game.get_dimension() - game.get_car('X').get_col()

    def h2(self, game: Game) -> int:
        """Heuristic 2: returns the number of cars in the way of the red car"""
        cars_in_way = 0
        for j in range(game.get_car('X').get_col() + 1, game.dimension + 1):
            cars_in_way += (game.board[(game.get_car('X').get_row(), j)]
                            not in ['X', '_'])
        return cars_in_way

    def h3(self, game: Game) -> int:
        """Heuristic 3

        Returns the amount of cars blocking the red car and adds 1 per car
        if those cars are blocked as well.
        """

        # Set red car row and col
        red_car_row = game.get_car('X').get_row()
        red_car_col = game.get_car('X').get_col()

        # Get cars in the way
        cars_in_way = 0
        for col_num in range(red_car_col + 1, game.dimension + 1):
            car_name = game.board[(red_car_row, col_num)]
            if car_name not in ['X', '_']:
                cars_in_way += 1
                cars_in_way = self.get_blocking_cars_value(cars_in_way,
                                                           car_name, game,
                                                           col_num)

        return cars_in_way

    def get_blocking_cars_value(self, cars_in_way: int, car_name: str,
                                game: Game, col_num: int) -> int:
        """Get the blocking value of a specific car

        If a car can not directly be moved, add 1 to cars_in_way
        If a car is horizontal, return maxsize (unsolvable)
        """

        # Set car
        car = game.get_car(car_name)

        # Get car specifics
        car_orientation = car.get_orientation()
        car_row = car.get_row()
        car_length = car.get_length()

        # Return blocking cars via cars_in_way
        if car_orientation == 'H':
            return sys.maxsize
        elif car_row > 1 and car_row + car_length < game.dimension:
            cars_in_way += (game.board[(car_row - 1, col_num)] != '_' or
                            game.board[(car_row + car_length, col_num)] != '_')
        elif car_row > 1:
            cars_in_way += (game.board[(car_row - 1, col_num)] != '_')
        elif car_row + car_length < game.dimension:
            cars_in_way += (game.board[(car_row + car_length, col_num)] != '_')
        else:
            return sys.maxsize
        return cars_in_way

    def solve(self, game: Game) -> Game:
        """Solve the game"""

        # Reinitialise for reruns
        self.re_init()

        # Get solution and return
        game = self.get_solution(game)
        return game

    def get_solution(self, game: Game) -> Game:
        """Get the full (best) solution via heuristic search"""

        # Add original board to open_set, moves_cost and parents
        self.open_set.put((0, 0, game.tuple_form()))
        self.moves_cost = {game.tuple_form(): 0}
        self.parents = Parents(game.tuple_form())

        # While games in queue, do an astar search
        while not self.open_set.empty():
            # Gets (using PriorityQueue) the node with lowest fscore
            _, cost, current_state = self.open_set.get()

            # Move to that state of the game
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

            # Print game if print_states is True
            if game.get_print_states():
                game.show_board()

            # If the game is won, print the length
            if game.is_won():
                game.set_moves(self.get_best_path(game))
                return game

            # Mark the current state as visited by adding to closed_set
            self.closed_set.add(current_state)

            # Get possible moves from current state and store the moves (cost)
            moves_list = self.get_possible_moves(game)
            moves_current_state = self.moves_cost[game.tuple_form()]

            # Move in all directions from current state
            for move in moves_list:
                # Move car
                car_name, direction = move
                game.move(car_name, direction)

                # If state not visited before:
                if game.tuple_form() not in self.closed_set:
                    move_cost = moves_current_state + 1
                    if game.tuple_form() not in self.moves_cost or \
                            move_cost < self.moves_cost[game.tuple_form()]:
                        self.moves_cost[game.tuple_form()] = move_cost
                        priority = move_cost + self.heuristic(game)
                        self.open_set.put((priority, move_cost,
                                           game.tuple_form()))
                        self.parents.add(game.tuple_form(), current_state)

                # Undo move to return to state
                game.move(car_name, self.reverse_direction(direction))

                # Remove unnecessary moves
                game.moves.pop()
                game.moves.pop()

        # If game not returned yet, game unsolvable
        raise Exception('The game can not be solved via astar + heuristics!')

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
            car_length = game.get_car(car_name).get_length()
            if abs(changed_places[1] - changed_places[0]) == car_length or \
                abs(changed_places[0] - changed_places[1])\
                    == game.dimension * car_length:
                moves_list.append((car_name, sign))
            else:
                raise Exception('Unobtainable move, something went wrong!')
            game_tuple = self.parents.get(game_tuple)

        # Reverse the list of moves
        moves_list.reverse()

        return moves_list

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


class Parents:

    def __init__(self, root: tuple[str, ...]) -> None:
        """Initialise Parents, a read and write implemenation of nodes"""
        self.parents: dict[tuple[str, ...], tuple[str, ...]] = {root: ()}

    def add(self, child: tuple[str, ...],
            parent: tuple[str, ...]) -> None:
        """Add child and parent to Parents"""
        self.parents[child] = parent

    def get(self, child: tuple[str, ...]) -> tuple[str, ...]:
        """Get parent based on child"""
        return self.parents[child]

    def is_in(self, child: tuple[str, ...]) -> bool:
        """Check if child is in Parents"""
        return child in self.parents
