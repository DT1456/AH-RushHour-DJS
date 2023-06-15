from game import Game
import random as random
from typing import Union
import copy

class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = ['L', 'R', 'U', 'D']
        self.graph: dict[str, list[tuple[str, list[str, str]]]] = {} # board_str als key. Value: [board_str, move = [A, L]]

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        if len(self.graph) == 0:
            self.fill_graph(game)
        moves_dict = self.get_possible_moves(game)
        car_name, direction = random.SystemRandom().choices(list(moves_dict))[0]
        game.move(car_name, direction)

        return game
        
    def get_possible_moves(self, game: Game) -> list:
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list
        
    def reverse_direction(self, direction: str) -> str:
        reverse_direction = 'L'
        if direction == 'L':
            reverse_direction  = 'R'
        elif direction == 'U':
            reverse_direction = 'D'
        elif direction == 'D':
            reverse_direction = 'U'
        
        return reverse_direction
        
    def fill_graph(self, game: Game) -> None:
        # Fill graph with all possible states
        self.graph[str(game)] = [('', ['', ''])]
        print(game)
        moves_list = self.get_possible_moves(game)
        new_games: set[Game] = set()
        old_game_str = str(game)
        for move in moves_list:
            car_name, direction = move
            game.move(car_name, direction)
            
            if str(game) not in self.graph:
                print('new', car_name, direction)
                self.graph[str(game)] = [(old_game_str, (car_name, direction))]
                new_games.add(game.cars)
            elif (old_game_str, (car_name, direction)) not in self.graph[str(game)]:
                print('exists', car_name, direction)
                self.graph[str(game)].append((old_game_str, (car_name, direction)))
                new_games.add(game.cars)
                
            game.move(car_name, self.reverse_direction(direction))
        print(len(new_games))
        for cars in new_games:
            print(cars)
        
        
        #print(self.graph)

