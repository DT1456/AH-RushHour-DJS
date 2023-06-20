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
        """Moving to different board state"""
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

    def solve(self, game: Game) -> Game:
        self.queue.enqueue(str(game))
        self.visited = set()
        self.parents = {str(game): None}
        self.original_board = str(game)
        self.parents_move = {str(game): None}

        while self.queue.size() > 0:
            # Remove first item from queue
            current_state = self.queue.dequeue()

            # Move to current state
            game = self.move_to_state(game, current_state)

            # WON? QUIT (TO DO: CHANGES MOVES?)
            if game.is_won():
                # USE self.parents here
                return game
            
            # Mark current state as visited
            self.visited.add(current_state)

            moves_list = self.get_possible_moves(game)

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)

                # Add str(game) to queue
                if str(game) not in self.visited:
                    self.queue.enqueue(str(game))
                    self.visited.add(str(game))
                    self.parents[str(game)] = current_state
                    self.parents_move[str(game)] = move
                # Go back to current state
                game.move(car_name, self.reverse_direction(direction))
        
        raise Exception('No solution found!\n')