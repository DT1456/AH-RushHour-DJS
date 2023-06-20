from game import Game
import random as random
import sys
from queue import PriorityQueue


class Solver:

    def __init__(self) -> None:
        """Initialises Astar solver

        Use a PriorityQueue for prioritising the next state
        Store parents and moves in dict(s) for getting the correct solution
        Use an open and closed set for marking states as open and closed
        """
        self.open_set = PriorityQueue()
        self.closed_set = set()
        self.moves_cost: dict[str, int]
        self.parents: dict[str, str]
        self.parents_move: dict[str, str]

    def heuristic(self, game: Game) -> int:
        """Runs the actual heuristic(s)"""
        return self.h0(game)

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
            cars_in_way += (game.board[(game.cars['X'].get_row(), j)] not in ['X', '_'])
        return cars_in_way

    def h3(self, game: Game) -> int:
        """Heuristic 3

        Returns the amount of cars blocking the red car and adds 1 if those
        cars are blocked as well.
        """
        red_car_row = game.cars['X'].get_row()
        red_car_col = game.cars['X'].get_col()

        cars_in_way = 0
        for j in range(red_car_col + 1, game.dimension + 1):
            car_name = game.board[(red_car_row, j)]
            if car_name not in ['X', '_']:
                cars_in_way += 1
                if game.cars[car_name].get_orientation() == 'H':
                    return sys.maxsize
                elif game.cars[car_name].get_row() > 1 and game.cars[car_name].get_row() + game.cars[car_name].get_length() < game.dimension:
                    cars_in_way += (game.board[(game.cars[car_name].get_row() - 1, j)] != '_' or game.board[(game.cars[car_name].get_row() + game.cars[car_name].get_length(), j)] != '_')
                elif game.cars[car_name].get_row() > 1:
                    cars_in_way += (game.board[(game.cars[car_name].get_row() - 1, j)] != '_')
                elif game.cars[car_name].get_row() + game.cars[car_name].get_length() < game.dimension:
                    cars_in_way += (game.board[(game.cars[car_name].get_row() + game.cars[car_name].get_length(), j)] != '_')
                else:
                    return sys.maxsize
        return cars_in_way


    def solve(self, game: Game) -> Game:
        game = self.get_solution(game)
        return game

    def get_solution(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        self.open_set.put((0, 0, game.tuple_form()))
        self.moves_cost = {game.tuple_form(): 0}
        self.parents = {game.tuple_form(): None}
        self.parents_move = {game.tuple_form(): None}

        while not self.open_set.empty():
            # Gets (using PriorityQueue) the node with lowest fscore
            _, cost, current_state = self.open_set.get()

            # Move to that state of the game
            game.set_game_via_str(current_state)

            # If the game is won, print the length
            if game.is_won():
                game.set_best_solution_steps(self.get_steps(game.tuple_form()))
                return game

            # Mark the current state as visited by adding to closed_set
            self.closed_set.add(current_state)

            # Get possible moves from current state and store the moves (for cost)
            moves_list = self.get_possible_moves(game)
            moves_current_state = self.moves_cost[game.tuple_form()]

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)
    
                # If state not visited before:
                if game.tuple_form() not in self.closed_set:
                    move_cost = moves_current_state + 1
                    if game.tuple_form() not in self.moves_cost or move_cost < self.moves_cost[game.tuple_form()]:
                        self.moves_cost[game.tuple_form()] = move_cost
                        priority = move_cost + self.heuristic(game)
                        self.open_set.put((priority, move_cost, game.tuple_form()))
                        self.parents[game.tuple_form()] = current_state
                        self.parents_move[game.tuple_form()] = move
                game.move(car_name, self.reverse_direction(direction))
        raise Exception('The game can not be solved via our a star + heuristics!')

    def get_steps(self, game_str):
        if self.parents[game_str] is not None:
            game_str = self.parents[game_str]
            return self.get_steps(game_str) + 1
        return 0

    def get_best_path(self, current_board_str, moves_list = []):
        if self.parents[current_board_str] is not None:
            moves_list.append(self.parents_move[current_board_str])
            current_board_str = self.parents[current_board_str]
            return self.get_best_path(current_board_str, moves_list)
        moves_list.reverse()
        return moves_list

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
        """Get list of possible moves in this state"""

        # Initialise moves_list as an empty list of possible moves
        moves_list = []

        # For all cars, try both moves and add them to moves if valid
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in [-1, 1]:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))

        # Return the filled list of moves
        return moves_list

    def reverse_direction(self, direction: int) -> int:
        """Defining and returning a reversed direction"""
        return -direction
