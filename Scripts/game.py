from car import Car

class Game:
    
    def __init__(self, file_name: str) -> None:
        self.cars: dict[str, Car]= {}
        self.load_cars(file_name)


    def load_cars(self, file_name: str) -> None:
        """Loads the cars from file_name"""
        with open(file_name) as f:
            f.readline()

            while True:
                line = f.readline().strip('\n')
                if line == '':
                    break
                car, orientation, col, row, length = line.split(',')
                self.cars[car] = Car(orientation, int(col), int(row), int(length))



if __name__ == '__main__': 
    g = Game('/home/sabrinastrijker/AH/AH-RushHour-DJS/Input/Rushhour6x6_1.csv')
    print(g.cars['X'])


