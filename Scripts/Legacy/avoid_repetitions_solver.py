from game import Game
import random.SystemRandom as random_pick


class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = ['L', 'R', 'U', 'D']

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        while True:
            # Pick a random car and a random direction
            car_name = random_pick().choice(list(game.get_cars()))
            direction = random_pick().choice(self.possible_directions)

            # Repick if same car & opposing direction (repetition)
            if len(game.get_moves()) > 0:
                last_car, last_direction = game.get_moves()[-1]
                while car_name == last_car and direction == last_direction:
                    # Repick a random car and a random direction
                    car_name = random_pick().choice(list(game.get_cars()))
                    direction = random_pick().choice(self.possible_directions)

            # If the chosen car and direction represent a valid move, move
            if game.move(car_name, direction):
                break

        return game
