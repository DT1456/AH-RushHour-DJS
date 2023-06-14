from game import Game
import random as random
from typing import Union


class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = ['L', 'R', 'U', 'D']

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        moves_dict = self.get_scores(self.get_possible_moves(game), game)
        car_name, direction = random.SystemRandom().choices(list(moves_dict), weights = moves_dict.values())[0]
        if 1 == 0:
            print('---------------------------')
            print(moves_dict)
            print(car_name, direction, len(moves_dict), moves_dict[(car_name, direction)])
        game.move(car_name, direction)

        return game
        
    def get_possible_moves(self, game: Game) -> list:
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list
        
    def get_scores(self, moves_list: list[tuple[str, str]], game: Game) -> dict[tuple[str, str], float]:
        moves_dict = {}
        for move in moves_list:
            car_name, direction = move
            score, game = self.get_score(car_name, direction, game)
            moves_dict[(car_name, direction)] = score
        return moves_dict
        
    def get_score(self, car_name: str, direction: str, game: Game) -> list[Union[float, Game]]:
        # play move
        game.move(car_name, direction)
        
        # calculate score
        score = 0
        score += game.dimension - game.cars['X'].col
        
        score = 1 / score
        
        # undo move
        game.move(car_name, self.reverse_direction(direction))
        
        # return game
        return [score, game]
        
    def reverse_direction(self, direction: str) -> str:
        reverse_direction = 'L'
        if direction == 'L':
            reverse_direction  = 'R'
        elif direction == 'U':
            reverse_direction = 'D'
        elif direction == 'D':
            reverse_direction = 'U'
        
        return reverse_direction
