from game import Game
import random as random
from queue import PriorityQueue
import sys

class Solver:

    def __init__(self) -> None:
        self.open_set = PriorityQueue()
        self.closed_set = set()
        self.moves_cost: dict[str, int]
        self.parents: dict[str, str]
        self.parents_move: dict[str, str]
        self.original_board: str

    def heuristic(self, game: Game):
        #return self.h2(game) + self.h3(game)
        #return self.h1(game)
        #return self.h2(game)
        #return self.h3(game)
        return self.h4(game)
        
    def h1(self, game: Game) -> int:
        return 0

    def h2(self, game: Game) -> int:
        return game.dimension - game.cars['X'].get_col()
        
    def h3(self, game: Game) -> int:
        cars_in_way = 0
        for j in range(game.cars['X'].get_col() + 1, game.dimension + 1):
            cars_in_way += (game.board[(game.cars['X'].get_row(), j)] not in ['X', '_'])
        return cars_in_way
        
    def h4(self, game: Game) -> int:
        red_car_row = game.cars['X'].get_row()
        red_car_col = game.cars['X'].get_col()
        print(game)
        cars_in_way = 0
        for j in range(red_car_col + 1, game.dimension + 1):
            car_name = game.board[(red_car_row, j)] 
            if car_name not in ['X', '_']:
                print(car_name, 'before cars_in_way: ', cars_in_way)
                cars_in_way += 1
                if game.cars[car_name].get_orientation() == 'V':
                    return sys.maxsize
                elif game.cars[car_name].get_row() > 1 and game.cars[car_name].get_row() + game.cars[car_name].get_length() < self.dimension:
                    cars_in_way += (game.board[(game.cars[car_name].get_row() - 1, j)] != '_' or game.board[(game.cars[car_name].get_row() + game.cars[car_name].get_length(), j)] != '_') 
                elif game.cars[car_name].get_row() > 1:
                    cars_in_way += (game.board[(game.cars[car_name].get_row() - 1, j)] != '_')
                elif game.cars[car_name].get_row() + game.cars[car_name].get_length() < self.dimension:
                    cars_in_way += (game.board[(game.cars[car_name].get_row() + game.cars[car_name].get_length(), j)] != '_')
                else:
                    return sys.maxsize
                print(car_name, 'after cars_in_way: ', cars_in_way)
                print(1/0)
        print(cars_in_way)
        print(1/0)
        return cars_in_way
        

    def solve(self, game: Game) -> Game:
        game = self.get_solution(game)
        print(len(game.moves))
        game.moves = []
        for move in self.get_best_path(str(game)):
            car_name, direction = move
            game.moves.append([car_name, game.direction_to_int(direction)])
        return game

    def get_solution(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        self.open_set.put((0, 0, str(game)))
        self.moves_cost = {str(game): 0}
        self.parents = {str(game): None}
        self.parents_move = {str(game): None}
        self.original_board = str(game)

        while not self.open_set.empty():
            # Gets (using PriorityQueue) the node with lowest fscore
            _, cost, current_state = self.open_set.get()

            # Move to that state of the game
            game = self.move_to_state(game, current_state)
            
            # If the game is won, print the length
            if game.is_won():
                return game

            # Mark the current state as visited by adding to closed_set
            self.closed_set.add(current_state)

            # Get possible moves from current state and store the moves (for cost)
            moves_list = self.get_possible_moves(game)
            moves_current_state = self.moves_cost[str(game)]

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)
                
                # If state not visited before:
                if str(game) not in self.closed_set:
                    move_cost = moves_current_state + 1
                    if str(game) not in self.moves_cost or move_cost < self.moves_cost[str(game)]:
                        self.moves_cost[str(game)] = move_cost
                        priority = move_cost + self.heuristic(game)
                        self.open_set.put((priority, move_cost, str(game)))
                        self.parents[str(game)] = current_state
                        self.parents_move[str(game)] = move
                game.move(car_name, self.reverse_direction(direction))
        raise Exception('The game can not be solved via our a star + heuristics!')

    def move_to_state(self, game: Game, state: str) -> Game:
        # move back
        while str(game) != self.original_board:
            move = self.parents_move[str(game)]
            car_name, direction = move
            game.move(car_name, self.reverse_direction(direction))
            
        # fill forward moves
        moves_forward = []
        
        while self.original_board != state:
            moves_forward.append(self.parents_move[state])
            state = self.parents[state]
            
        # move forward
        moves_forward.reverse()
        for move in moves_forward:
            car_name, direction = move
            game.move(car_name, direction)
            

        return game

    def get_best_path(self, current_board_str, moves_list = []):
        if self.parents[current_board_str] is not None:
            moves_list.append(self.parents_move[current_board_str])
            current_board_str = self.parents[current_board_str]
            return self.get_best_path(current_board_str, moves_list)
        moves_list.reverse()
        return moves_list

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
        """Get list of possible moves in this state"""
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list
        
    def reverse_direction(self, direction: str) -> str:
        """Defining and returning a reversed direction"""
        reverse_direction = 'L'
        if direction == 'L':
            reverse_direction = 'R'
        elif direction == 'U':
            reverse_direction = 'D'
        elif direction == 'D':
            reverse_direction = 'U'

        return reverse_direction
