from game import Game



class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = ['L', 'R', 'U', 'D']

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        while True:
            # Pick a random car and a random direction
            car_name = random.SystemRandom().choice(list(game.cars))
            direction = random.SystemRandom().choice(self.possible_directions)

            # If the chosen car and direction represent a valid move, move
            if game.move(car_name, direction):
                break

        return game
