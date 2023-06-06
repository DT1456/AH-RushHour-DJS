from game import Game
import random as random

class Solver:

    def __init__(self):
        pass
        
    	
    def play_move(self, game: Game):
        car_name = random.choice(list(game.cars))
        direction = random.choice(['l', 'r', 'u', 'd'])
        while not game.move(car_name, direction):
            car_name = random.choice(list(game.cars))
            direction = random.choice(['l', 'r', 'u', 'd'])

        return game
