from game import Game
import random as random


class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = [-1, 1]
        self.visited_states: set[str] = set()

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        if len(self.visited_states) == 0:
            self.visited_states = set(str(game))

        moves_list = self.get_possible_moves(game)

        # Pick a random car and a random direction
        move = random.SystemRandom().choice(moves_list)
        car_name, direction = move
        game.move(car_name, direction)
        
        while str(game) in self.visited_states and len(moves_list) > 1:
            moves_list.remove(move)
            game.move(car_name, self.reverse_direction(direction))
            move = random.SystemRandom().choice(moves_list)
            car_name, direction = move
            game.move(car_name, direction)
        
        if len(moves_list) == 1:
            move = random.SystemRandom().choice(moves_list)
            car_name, direction = move
            game.move(car_name, direction)
        self.visited_states.add(str(game))

        return game
        
    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
        """Get list of possible moves in this state"""
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in [-1, 1]:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list

    def reverse_direction(self, direction: str) -> str:
        """Defining and returning a reversed direction"""
        return -direction
