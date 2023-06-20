from game import Game

class Queue:

    # Initialiase empty queue
    def __init__(self):
        self._data = []

    # Add element to back of queue
    def enqueue(self, element):
        self._data.append(element) 

    # Remove and return element from front of queue
    def dequeue(self):
        assert self.size() > 0
        return self._data.pop(0)

    # find and return size of the queue
    def size(self):
        return len(self._data)

class Solver:
    def __init__(self):
        self.parents: dict[str, str]
        self.queue = Queue()
        self.original_board: str
        self.parents_move: dict[str, tuple[str, str]]

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
        """Get list of possible moves in this state"""
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list
        
    def reverse_direction(self, direction: str) -> str:
        """Defining and returning a reversed direction"""
        reverse_direction = 'L'
        if direction == 'L':
            reverse_direction = 'R'
        elif direction == 'U':
            reverse_direction = 'D'
        elif direction == 'D':
            reverse_direction = 'U'

        return reverse_direction