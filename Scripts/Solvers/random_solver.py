from game import Game
import random as random


class Solver:

    def __init__(self) -> None:
        pass

    def solve(self, game: Game) -> Game:
        while not game.is_won():
            game = self.play_move(game)
        return game

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        moves_list = self.get_possible_moves(game)
        # Pick a random car and a random direction
        move = random.SystemRandom().choice(moves_list)
        car_name, direction = move
        game.move(car_name, direction)

        return game

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
        """Get list of possible moves in this state"""
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list
