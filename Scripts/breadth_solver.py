from game import Game



class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.states: dict[str, list[tuple[str]]] = {}

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
        self.states[game.__str__] = ()
        old_game_str = game.__str__

        moves_list = self.get_possible_moves(game)
        for move in moves_list:
            game.move(move[0], move[1])
            if game.__str__ not in self.states:
                self.states[game.__str__] = move
            elif len(self.states[game.__str__]) > len(self.states[old_game_str] + move):
                self.states[game.__str__] = self.states[old_game_str] + move

            reverse_direction = self.reverse_direction(move[1])
            game.move(move[0], reverse_direction)
    
    def get_possible_moves(self, game: Game) -> list:
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append(car_name, direction)
        return moves_list