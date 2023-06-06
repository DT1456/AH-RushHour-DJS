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
            board_string += ' _ ' * self.dimension + '\n'

        return board_string 

if __name__ == '__main__': 
    g = Game('/home/sabrinastrijker/AH/AH-RushHour-DJS/Input/Rushhour6x6_1.csv', 6)
    print(g.cars['X'])

    print(g.is_won())

    print(g.__str__())


