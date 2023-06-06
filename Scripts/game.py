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
        if self.cars[car_name].orientation == 'H':
            if direction not in ['L', 'R']:
                return False
        else:
            if direction not in ['U', 'D']:
                return False
        # check if empty space (dus ook dimensie bord)
        try:
            if direction == 'U':
                location_x = self.cars[car_name].row - 1
                location_y = self.cars[car_name].col
            elif direction == 'D':
                location_x = self.cars[car_name].row + self.cars[car_name].length
                location_y = self.cars[car_name].col
            elif direction == 'L':
                location_x = self.cars[car_name].row
                location_y = self.cars[car_name].col - 1
            elif direction == 'R':
                location_x = self.cars[car_name].row
                location_y = self.cars[car_name].col + self.cars[car_name].length
            else:
                return False
            if self.board[(location_x, location_y)] != '_':
                return False
        except:
            return False
        return True

    def move(self, car_name: str, direction: str) -> bool:
        direction = direction.upper()
        if self.is_valid_move(car_name, direction):
            # adjust empty space (eentje erbij, eentje eraf)
            if direction == 'U':
                location_x = self.cars[car_name].row - 1
                location_y = self.cars[car_name].col
                self.board[(location_x, location_y)] = car_name
                self.board[(location_x + self.cars[car_name].length, location_y)] = '_'
            elif direction == 'D':
                location_x = self.cars[car_name].row + self.cars[car_name].length
                location_y = self.cars[car_name].col
                self.board[(location_x, location_y)] = car_name
                self.board[(self.cars[car_name].row, location_y)] = '_'
            elif direction == 'L':
                location_x = self.cars[car_name].row
                location_y = self.cars[car_name].col - 1
                self.board[(location_x, location_y)] = car_name
                self.board[(location_x, location_y  + self.cars[car_name].length)] = '_'
            else:
                location_x = self.cars[car_name].row
                location_y = self.cars[car_name].col + self.cars[car_name].length
                self.board[(location_x, location_y)] = car_name
                self.board[(location_x, self.cars[car_name].col)] = '_'
    	    
    	    # adjust car.col of car.row
            self.cars[car_name].row += (direction == 'D') - (direction == 'U')
            self.cars[car_name].col += (direction == 'R') - (direction == 'L')
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

    print(g)
    while not g.is_won():
        car_name, direction = input("What car to move? Carname and direction split by space!\n").split()
        car_name = car_name.upper()
        if g.move(car_name, direction):
            print(g)
        else:
            print("Invalid move!")