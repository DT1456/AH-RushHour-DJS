from car import Car

class Game:
    
    def __init__(self, file_name: str, dimension: int) -> None:
        self.cars: dict[str, Car]= {}
        self.load_cars(file_name)
        self.dimension = dimension
        self.board: dict[tuple[int, int], str] = {}
        self.load_board()
        

    def load_board(self) -> None:
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.board[(i + 1, j + 1)] = '_'
                
        for car_name, Car in zip(self.cars, self.cars.values()):
            if Car.orientation == 'H':
                for k in range(Car.length):
                    self.board[(Car.row, Car.col + k)] = car_name
            else:
                for k in range(Car.length):
                    self.board[(Car.row + k, Car.col)] = car_name

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

    def is_valid_move(self, car_name: str, direction: str) -> bool:
    # check if direction correct
        if self.cars[car_name].direction == 'H':
            if direction not in ['L', 'R']:
                return False
        else:
            if direction not in ['U', 'D']:
                return False
        # check if empty space (dus ook dimensie bord)
        try:
            if self.board[(self.cars[car_name].row - (direction == 'U') + (direction == 'D'), self.cars[car_name].col - (direction == 'L') + (direction == 'R'))] != '_':
                return False
        except:
            return False
        return True


    def move(self, car_name: str, direction: str) -> bool:
        direction = direction.upper()
        if self.is_valid_move(car_name, direction):
    	    # adjust car.col of car.row
    	    # adjust empty space (eentje erbij, eentje eraf)
            return True
        return False
    

    def __str__(self) -> str:
        board_string = ''
        for i in range(self.dimension):
            for j in range(self.dimension):
                board_string += ' ' + self.board[(i + 1, j + 1)] + ' '
            board_string += '\n\n'
        
        return board_string
    
     

if __name__ == '__main__': 
    g = Game('/home/sabrinastrijker/AH/AH-RushHour-DJS/Input/Rushhour6x6_1.csv', 6)
    print(g.cars['X'])

    print(g.is_won())

    print(g.__str__())

