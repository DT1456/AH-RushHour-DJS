from game import Game
import sys
import os

# set recusion limit
sys.setrecursionlimit(10000)


class Queue:

    def __init__(self) -> None:
        """Initialising the empty queue"""
        self.counter_reader = 0
        self.writer_counter = 0

    def enqueue(self, element: tuple[str, ...]) -> None:
        """Adding element to back of queue"""
        self.writer_counter += 1
        with open('Solvers/Queues/queue' + str(self.writer_counter) + '.txt', 'w') as f:
            for e in element:
                f.write(e + ',')
            f.write('\n')

    def dequeue(self) -> tuple[str, ...]:
        """Remove and return element from front of queue"""
        self.counter_reader += 1
        with open('Solvers/Queues/queue' + str(self.counter_reader) + '.txt', 'r') as f:
            last_line = f.readline()

        os.remove('Solvers/Queues/queue' + str(self.counter_reader) + '.txt')
        
        last_line = last_line.split(',')
        last_line = tuple(last_line[:len(last_line)-1])
        
        return last_line

    def is_big_enough(self) -> bool:
        """Find and return size of queue"""
        return self.writer_counter > self.counter_reader


class Queue1:

    def __init__(self) -> None:
        """Initialising the empty queue"""

        self._data: list[tuple[str, ...]] = []

    def enqueue(self, element: tuple[str, ...]) -> None:
        """Adding element to back of queue"""

        self._data.append(element)

    def dequeue(self) -> tuple[str, ...]:
        """Remove and return element from front of queue"""

        assert self.size() > 0
        return self._data.pop(0)

    def size(self) -> int:
        """Find and return size of queue"""
        return len(self._data)
        
    def is_big_enough(self) -> bool:
        return self.size() > 0


class VisitedStates:
    def __init__(self):
        self.bucket_count = 10000
        for i in range(self.bucket_count):
            with open('Solvers/VisitedStates/' + str(i), 'w') as f:
                pass

    def add(self, game_tuple):
        file_name = hash(game_tuple) % self.bucket_count
        with open('Solvers/VisitedStates/' + str(file_name), 'a') as f:
            for k in game_tuple:
                f.write(k + ',')
            f.write('\n')
    
    def is_in(self, game_tuple):
        file_name = hash(game_tuple) % self.bucket_count
        with open('Solvers/VisitedStates/' + str(file_name), 'r') as f:
            while True:
                line = f.readline().split(',')
                line = tuple(line[:len(line)-1])
                if len(line) == 0:
                    return False
                if line == game_tuple:
                    return True


class Solver:

    def __init__(self) -> None:
        """Initialising parent states dict, queue and original board"""
        if not os.path.exists('Solvers/VisitedStates'):
            os.system('mkdir Solvers/VisitedStates')
        self.queue = Queue()
        self.original_board: tuple[str, ...]
        self.winning_state: tuple[str, ...] = ()

    def get_possible_moves(self, game: Game) -> list[tuple[str, int]]:
        """Get list of possible moves in this state"""

        # Initialise moves_list as an empty list of possible moves
        moves_list = []

        # For all cars, try both moves and add them to moves if valid
        for car_name in game.get_cars():
            for direction in [-1, 1]:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))

        # Return the filled list of moves
        return moves_list

    def reverse_direction(self, direction: int) -> int:
        """Defining and returning a reversed direction"""

        return -direction

    def solve(self, game: Game) -> Game:
        """Counting states"""

        self.queue.enqueue(game.tuple_form())
        self.visited_states = VisitedStates()

        while self.queue.is_big_enough() > 0:
            # Remove first item from queue
            current_state = self.queue.dequeue()

            # Move to current state
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

            # If game is won, quit and set best solution steps for game
            if self.winning_state == () and game.is_won():
            	self.winning_state = game.tuple_form()

            moves_list = self.get_possible_moves(game)

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)

                # Add game.tuple_form() to queue
                if not self.visited_states.is_in(game.tuple_form()):
                    self.queue.enqueue(game.tuple_form())
                    self.visited_states.add(game.tuple_form())

                # Go back to current state
                game.move(car_name, self.reverse_direction(direction))

                # Remove unnecessary moves
                game.moves.pop()
                game.moves.pop()

        # Cleanup
        os.system('rm -r Solvers/VisitedStates')
        os.system('mkdir Solvers/VisitedStates')
        if self.winning_state == ():
            raise Exception('Something went wrong, game not solvable!\n')
        else:
            return game
