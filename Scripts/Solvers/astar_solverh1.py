from game import Game
from queue import PriorityQueue
import sys
from typing import Union


class Solver:

    def __init__(self) -> None:
        """Initialises Astar solver

        Use a PriorityQueue for prioritising the next state
        Store parents and moves in dict(s) for getting the correct solution
        Use an open and closed set for marking states as open and closed
        """
        self.open_set: PriorityQueue[tuple[int, int, tuple[str, ...]]] = PriorityQueue()
        self.closed_set: set[tuple[str, ...]] = set()
        self.moves_cost: dict[tuple[str, ...], int]
        self.parents: dict[tuple[str, ...], tuple[str, ...]]

    def heuristic(self, game: Game) -> int:
        """Runs the actual heuristic(s)"""
        return self.h1(game)

    def h0(self, game: Game) -> int:
        """Heuristic 0: always returns zero"""
        return 0

    def h1(self, game: Game) -> int:
        """Heuristic 1: returns the distance of red car to exit"""
        return game.dimension - game.cars['X'].get_col()

    def h2(self, game: Game) -> int:
        """Heuristic 2: returns the number of cars in the way of the red car"""
        cars_in_way = 0
        for j in range(game.cars['X'].get_col() + 1, game.dimension + 1):
            cars_in_way += (game.board[(game.cars['X'].get_row(), j)]
                            not in ['X', '_'])
        return cars_in_way

    def h3(self, game: Game) -> int:
        """Heuristic 3

        Returns the amount of cars blocking the red car and adds 1 if those
        cars are blocked as well.
        """
        red_car_row = game.cars['X'].get_row()
        red_car_col = game.cars['X'].get_col()

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
        car = game.cars[car_name]

        # Get car specifics
        car_orientation = car.get_orientation()
        car_row = car.get_row()
        car_length = car.get_length()

        # Increment cars_in_way
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

        game = self.get_solution(game)
        return game

    def get_solution(self, game: Game) -> Game:
        """Get the full (best) solution via heuristic search"""
        self.open_set.put((0, 0, game.tuple_form()))
        self.moves_cost = {game.tuple_form(): 0}
        self.parents = {game.tuple_form(): ()}

        while not self.open_set.empty():
            # Gets (using PriorityQueue) the node with lowest fscore
            _, cost, current_state = self.open_set.get()

            # Move to that state of the game
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

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
                        self.parents[game.tuple_form()] = current_state
                game.move(car_name, self.reverse_direction(direction))
        raise Exception('The game can not be solved via astar + heuristics!')

    def get_steps(self, tuple_form: tuple[str, ...]) -> int:
        while self.parents[tuple_form] != ():
            tuple_form = self.parents[tuple_form]
            return self.get_steps(tuple_form) + 1
        return 0

    def get_best_path(self, game: Game) -> list[list[Union[int, str]]]:
        """Construct the best path based on parents, if game is won"""

        # If game is not won, exit
        if not game.is_won():
            raise Exception('Game not yet won, unable to get best path!')

        # Define game_tuple as current game state
        game_tuple = game.tuple_form()

        # Initialise the list of moves
        moves_list = []
        while self.parents[game_tuple] != ():
            # Set changed_places as list of places that were changed with the move
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
            elif changed_places[1] - changed_places[0] == game.dimension * car_length:
                # Car direction: up
                moves_list.append((car_name, 1))
            elif changed_places[0] - changed_places[1] == game.dimension * car_length:
                # Car direction: down
                moves_list.append((car_name, -1))
            else:
                raise Exception('Unobtainable move, something went wrong!')
            game_tuple = self.parents[game_tuple]

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
