from game import Game
import sys
import os
import random
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


class Solver:

    def __init__(self) -> None:
        """Initialising parent states dict, queue and original board"""

        self.queue = Queue()
        self.original_board: tuple[str, ...]

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
        """Searching for solution of the game"""

        self.queue.enqueue(game.tuple_form())
        self.parents = {game.tuple_form(): ()}
        self.original_board = game.tuple_form()
        #self.counter = 0

        while self.queue.is_big_enough():
            # Remove first item from queue
            current_state = self.queue.dequeue()
            #self.counter += 1
            #print(self.counter)

            # Move to current state
            game.set_game_via_str(current_state)
            game.increase_visited_state_count()

            # If game is won, quit and set best solution steps for game
            if game.is_won():
                game.set_moves(self.get_best_path(game))
                os.system('rm -r Solvers/Queues')
                os.system('mkdir Solvers/Queues')
                return game

            moves_list = self.get_possible_moves(game)

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)

                # Add game.tuple_form() to queue
                if game.tuple_form() not in self.parents:
                    self.queue.enqueue(game.tuple_form())
                    self.parents[game.tuple_form()] = current_state
                # Go back to current state
                game.move(car_name, self.reverse_direction(direction))

        raise Exception('No solution found!\n')

    def get_best_path(self, game: Game) -> list[tuple[str, int]]:
        """Construct the best path based on parents, if game is won"""

        # If game is not won, exit
        if not game.is_won():
            raise Exception('Game not yet won, unable to get best path!')

        # Define game_tuple as current game state
        game_tuple = game.tuple_form()

        # Initialise the list of moves
        moves_list = []
        while self.parents[game_tuple] != ():
            # Set changed_places as list of places that
            # were changed with the move
            changed_places = []

            # Go over the tuples to find differences
            for i in range(len(game_tuple)):
                if game_tuple[i] != self.parents[game_tuple][i]:
                    changed_places.append(i)

                    # Get the car_name
                    if game_tuple[i] == '_':
                        car_name = self.parents[game_tuple][i]
                    else:
                        car_name = game_tuple[i]

            # Based on changed_places, deduce the move that took place
            car_length = game.cars[car_name].get_length()
            if changed_places[1] - changed_places[0] == car_length:
                # Car direction: right
                moves_list.append((car_name, 1))
            elif changed_places[0] - changed_places[1] == car_length:
                # Car direction: left
                moves_list.append((car_name, -1))
            elif changed_places[1] - changed_places[0]\
                    == game.dimension * car_length:
                # Car direction: up
                moves_list.append((car_name, 1))
            elif changed_places[0] - changed_places[1]\
                    == game.dimension * car_length:
                # Car direction: down
                moves_list.append((car_name, -1))
            else:
                raise Exception('Unobtainable move, something went wrong!')
            game_tuple = self.parents[game_tuple]

        # Reverse the list of moves
        moves_list.reverse()

        return moves_list
