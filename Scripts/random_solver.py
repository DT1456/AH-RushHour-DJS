from game import Game
import random as random

if __name__ == '__main__': 
    g = Game('/home/duco/AH-RushHour-DJS/Input/Rushhour6x6_1.csv', 6)

    print(g)
    while not g.is_won():
        car_name = random.choice(list(g.cars))
        direction = random.choice(['l', 'r', 'u', 'd'])
        if g.move(car_name, direction):
            print(g)
        else:
            print("Invalid move!")
    print("Congrats!")
