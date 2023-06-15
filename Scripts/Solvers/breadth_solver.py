from game import Game


class Solver:

    def __init__(self) -> None:
        """Initializes dictionary of states and list of winning moves"""
        self.states: dict[str, list[tuple[str, str]]] = {}
        self.winning_moves: list[tuple[str, str]] = []
        self.found_winning = False

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

    def copy_states(self, state_dict: dict[str, tuple[str, str]],
                    length: int) -> dict[str, tuple[str, str]]:
        """Makes a copy of self.states that is named named state_dict"""
        for state in self.states:
            if len(self.states[state]) == length:
                state_dict[state] = self.states[state]
        return state_dict

    def fill_moves(self, moves_list: list[tuple[str, str]], moves_so_far: list[tuple[str, str]], game: Game):
        for move in moves_list:
            game.move(move[0], move[1])
            # If new state is found, put in dictionary with value
            # of all moves so far + most recent move
            if game.__str__() not in self.states:
                self.states[game.__str__()] = moves_so_far + [move]
            elif len(self.states[game.__str__()]) > len(moves_so_far
                                                        + [move]):
                print('nu wel')
                self.states[game.__str__()] = moves_so_far + [move]
            # When game is won, put all previous moves and
            # most recent move in list of winning moves.
            if game.is_won():
                self.found_winning = True
                self.winning_moves = moves_so_far + [move]
            reverse_direction = self.reverse_direction(move[1])
            game.move(move[0], reverse_direction)

    def fill_states(self, game: Game) -> None:
        """Fills all states until a series of winning moves is found.

        While the winning the series of winning moves hasn't been found yet
        this method will check each new state, and checks moves.
        If the state has already been visited a reversed move is made.
        When the game is won it will put all te moves that led to
        that win in a list of winning moves.
        """
        self.states[game.__str__()] = []
        length = 0

        while not self.found_winning:
            # Make copy of self.states
            state_dict = {}
            state_dict = self.copy_states(state_dict, length)

            for state in state_dict:
                moves_so_far = state_dict[state]
                # Make list with reversed directions
                moves_so_far_reversed = [(state[0],
                                         self.reverse_direction(state[1]))
                                         for state in moves_so_far]
                # Reverse list so last move becomes te first reversed move
                moves_so_far_reversed.reverse()

                # Move forward
                for move in moves_so_far:
                    game.move(move[0], move[1])

                moves_list = self.get_possible_moves(game)
                self.fill_moves(moves_list, moves_so_far, game)

                # Move backwards
                for move in moves_so_far_reversed:
                    game.move(move[0], move[1])
                # Break when game is won
                if self.found_winning:
                    break

            length += 1

    def get_possible_moves(self, game: Game) -> list[tuple[str, str]]:
        """Get list of possible moves in this state"""
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list

    def play_move(self, game: Game) -> Game:
        """Finds the series of winning moves and then plays one move"""
        # Checks if game is played (solved) yet
        if game.get_step_count() == 0 or len(self.states) == 0:
            # Reset solver
            self.states = {}
            self.winning_moves = []
            self.found_winning = False

            # Fill states
            self.fill_states(game)
            game.moves = []
        # Plays the winning moves
        if self.found_winning:
            move = self.winning_moves[0]
            game.move(move[0], move[1])
            self.winning_moves = self.winning_moves[1:]
        else:
            raise Exception('No solution found!')
        return game
