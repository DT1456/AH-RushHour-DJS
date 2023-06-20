from game import Game

class Queue:

    # Initialise empty queue
    def __init__(self):
        self._data = []

    # Add element to back of queue
    def enqueue(self, element):
        self._data.append(element) 

    # Remove and return element from front of queue
    def dequeue(self):
        assert self.size() > 0
        return self._data.pop(0)

    # Find and return size of the queue
    def size(self):
        return len(self._data)

class Solver:
    def __init__(self):
        # dict of states previous to current state (key) and current states
        self.parents: dict[str, str]
        self.queue = Queue()
        self.original_board: str
        # dict of moves that that take you from previous state to the current state
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
    
    def move_to_state(self, game: Game, state: str) -> Game:
        # Moving backwards
        while str(game) != self.original_board:
            move = self.parents_move[str(game)]
            car_name, direction = move
            game.move(car_name, self.reverse_direction(direction))
        
        # Fill forward moves
        moves_forward = []

        while self.original_board != state:
            moves_forward.append(self.parents_move[state])
            state = self.parents[state]
        
        # Move forwards

        # Reverse list put most recent move to front
        moves_forward.reverse()
        for move in moves_forward:
            car_name, direction = move
            game.move(car_name, direction)
        
        return game