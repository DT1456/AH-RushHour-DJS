from game import Game
import os
import sys

# set recusion limit
sys.setrecursionlimit(10000)


class Solver:

    def __init__(self) -> None:
        """Initialising Count States Solver

        Simply do a breadth-first search without stopping if game won
        Continue until queue is empty, then all states are visited
        """
        self.queue = Queue()
        self.original_board: tuple[str, ...]
        self.winning_state: tuple[str, ...] = ()

    def re_init(self) -> None:
        """Initialising parent states dict, queue and original board"""
        self.queue = Queue()
        self.winning_state = ()

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
        """Return reversed direction"""
        return -direction

    def solve(self, game: Game) -> Game:
        """Counting states"""

        # Reinitialise for reruns
        self.re_init()

        # Add starting state to queue, initialise visited_states
        self.queue.enqueue(game.tuple_form())
        self.visited_states = VisitedStates()

        while self.queue.is_big_enough() > 0:
            # Remove first item from queue
            current_state = self.queue.dequeue()

            # Move to current state
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

            # Print game if print_states is True
            if game.get_print_states():
                game.show_board()

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

        # Return game or raise Exception if no winning state found
        if self.winning_state == ():
            raise Exception('Something went wrong, game not solvable!\n')
        else:
            return game


class Queue:

    def __init__(self) -> None:
        """Initialising the queue: a read/write implementation"""
        self.counter_reader = 0
        self.writer_counter = 0

    def enqueue(self, element: tuple[str, ...]) -> None:
        """Adding element to back of queue"""

        # Increment counter
        self.writer_counter += 1

        # Add a new element to Queue by writing new file
        with open('Solvers/Queues/queue' + str(self.writer_counter) + '.txt',
                  'w') as f:
            for e in element:
                f.write(e + ',')
            f.write('\n')

    def dequeue(self) -> tuple[str, ...]:
        """Remove and return element from front of queue"""

        # Increment counter reader
        self.counter_reader += 1

        # Read correct file
        with open('Solvers/Queues/queue' + str(self.counter_reader) + '.txt',
                  'r') as f:
            line = f.readline()

        # Remove file (popping the queue)
        os.remove('Solvers/Queues/queue' + str(self.counter_reader) + '.txt')

        # Return tuple
        line_list = line.split(',')
        line_tuple = tuple(line_list[:len(line_list)-1])
        return line_tuple

    def is_big_enough(self) -> bool:
        """Find and return whether of queue is not zero"""
        return self.writer_counter > self.counter_reader


class VisitedStates:

    def __init__(self) -> None:
        """Initialise VisitedStates: a read/write implementation

        It is a replacement of visited_states as set() for memory saving
        """

        # Set amount of buckets
        self.bucket_count = 10000

        # Write empty buckets (as files)
        for i in range(self.bucket_count):
            with open('Solvers/VisitedStates/' + str(i), 'w'):
                pass

    def add(self, game_tuple: tuple[str, ...]) -> None:
        """Add a state to VisitedStates"""

        # Get file_name based on hash of game_tuple
        file_name = hash(game_tuple) % self.bucket_count

        # Add game_tuple to correct file
        with open('Solvers/VisitedStates/' + str(file_name), 'a') as f:
            for k in game_tuple:
                f.write(k + ',')
            f.write('\n')

    def is_in(self, game_tuple: tuple[str, ...]) -> bool:
        """Return whether a certain game_tuple is in VisitedStates"""

        # Get file_name based on hash of game_tuple
        file_name = hash(game_tuple) % self.bucket_count

        # Go over a bucket, check if game_tuple is in the file
        with open('Solvers/VisitedStates/' + str(file_name), 'r') as f:
            while True:
                line_list = f.readline().split(',')
                line_tuple = tuple(line_list[:len(line_list)-1])
                if len(line_tuple) == 0:
                    return False
                if line_tuple == game_tuple:
                    return True
