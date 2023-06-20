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

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
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

    def reverse_direction(self, direction: str) -> str:
        """Defining and returning a reversed direction"""
        return -direction

    def get_steps(self, game_str):
        steps = 0
        while game_str != self.original_board:
            steps += 1
            game_str = self.parents[game_str]
        return steps

    def solve(self, game: Game) -> Game:
        self.queue.enqueue(game.tuple_form())
        self.visited = set()
        self.parents = {game.tuple_form(): None}
        self.original_board = game.tuple_form()

        while self.queue.size() > 0:
            # Remove first item from queue
            current_state = self.queue.dequeue()

            # Move to current state
            game.set_game_via_str(current_state)

            # If game is won, quit and set best solution steps for game
            if game.is_won():
                game.best_solution_steps = self.get_steps(game.tuple_form())
                return game

            # Mark current state as visited
            self.visited.add(current_state)

            moves_list = self.get_possible_moves(game)

            # Move in all directions from current state
            for move in moves_list:
                car_name, direction = move
                game.move(car_name, direction)

                # Add game.tuple_form() to queue
                if game.tuple_form() not in self.visited:
                    self.queue.enqueue(game.tuple_form())
                    self.visited.add(game.tuple_form())
                    self.parents[game.tuple_form()] = current_state
                # Go back to current state
                game.move(car_name, self.reverse_direction(direction))

        raise Exception('No solution found!\n')
