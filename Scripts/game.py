from car import Car

class Game:
    
    def __init__(self, file_name: str, dimension: int) -> None:
        self.cars: dict[str, Car]= {}
        self.load_cars(file_name)
        self.dimension = dimension


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


    def is_won(self) -> bool: 
        return self.cars['X'].get_col() == self.dimension - 1


    def __str__(self) -> str:
        board_string = ''
        for _ in range(self.dimension):
            board_string += ' _ ' * self.dimension + '\n\n'

        for car_name, Car in zip(self.cars, self.cars.values()):
            
            if Car.orientation == 'H':
                board_string = board_string[:(Car.col - 1) * 3 + (Car.row - 1) * (2 + self.dimension * 3)] + (' ' + car_name + ' ') * Car.length + board_string[3 * (Car.col - 1 + Car.length) + (Car.row - 1) * (2 + self.dimension * 3):]
            else:
                for i in range(Car.length):
                    board_string = board_string[:(Car.col - 1) * 3 + (Car.row - 1 + i) * (2 + self.dimension * 3)] + (' ' + car_name + ' ') + board_string[3 * Car.col + (Car.row - 1 + i) * (2 + self.dimension * 3):]

        return board_string 

if __name__ == '__main__': 
    g = Game('/home/sabrinastrijker/AH/AH-RushHour-DJS/Input/Rushhour6x6_1.csv', 6)
    print(g.cars['X'])

    print(g.is_won())

    print(g.__str__())

