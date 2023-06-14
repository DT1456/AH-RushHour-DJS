from game import Game



class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.states: dict[str, list[tuple[str]]] = {}
        self.winning_moves = []
        self.found_winning = False

    def reverse_direction(self, direction: str) -> str:
        reverse_direction = 'L'
        if direction == 'L':
            reverse_direction  = 'R'
        elif direction == 'U':
            reverse_direction = 'D'
        elif direction == 'D':
            reverse_direction = 'U'
        
        return reverse_direction

    def fill_states(self, game: Game) -> None:
        self.states[game.__str__()] = []
        old_game_str = game.__str__()
        length = 0

        while not self.found_winning:
            state_lst = {}
            for state in self.states:
                if len(self.states[state]) == length:
                    state_lst[state] = self.states[state]

            for state in state_lst:
                moves_so_far = state_lst[state]
                moves_so_far_reversed = [(state[0], self.reverse_direction(state[1])) for state in moves_so_far]
                moves_so_far_reversed.reverse()

                # Move forward
                for move in moves_so_far:
                    game.move(move[0], move[1])
                old_game_str = game.__str__()

                moves_list = self.get_possible_moves(game)
                for move in moves_list:
                    game.move(move[0], move[1])
                    if game.__str__() not in self.states:
                        self.states[game.__str__()] = moves_so_far + [move]
                    if game.is_won():
                        self.found_winning = True
                        self.winning_moves = moves_so_far + [move]
                    reverse_direction = self.reverse_direction(move[1])
                    game.move(move[0], reverse_direction)

                # move backward
                for move in moves_so_far_reversed:
                    game.move(move[0], move[1])
                if self.found_winning:
                    break
            
            length += 1
    
    def get_possible_moves(self, game: Game) -> list:
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list

    def play_move(self, game: Game) -> Game:
        if len(self.states) == 0:
            self.fill_states(game)
            game.moves = []
        if self.found_winning:
            move = self.winning_moves[0]
            game.move(move[0], move[1])
            self.winning_moves = self.winning_moves[1:]
        else:
            raise Exception('No solution found!')
        return game
