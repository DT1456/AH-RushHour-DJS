from game import Game
import random as random
from typing import Union
import copy

class Solver:

    def __init__(self) -> None:
        """Initialise the possible directions to be chosen in every move"""
        self.possible_directions: list[str] = ['L', 'R', 'U', 'D']
        self.graph: dict[str, list[tuple[str, list[str, str]]]] = {} # board_str als key. Value: [board_str, move = [A, L]]
        self.winning_states: list[str] =  []

    def play_move(self, game: Game) -> Game:
        """Play one move in order to solve the game"""
        if len(self.graph) == 0:
            self.fill_graph(game)
        #HIER NOG: DAADWERKELIJK KORTSTE VINDEN
        return game
        
    def get_possible_moves(self, game: Game) -> list:
        moves_list = []
        for car_name, car in zip(game.cars, game.cars.values()):
            for direction in ['L', 'R', 'U', 'D']:
                if game.is_valid_move(car_name, direction):
                    moves_list.append((car_name, direction))
        return moves_list
        
    def reverse_direction(self, direction: str) -> str:
        reverse_direction = 'L'
        if direction == 'L':
            reverse_direction  = 'R'
        elif direction == 'U':
            reverse_direction = 'D'
        elif direction == 'D':
            reverse_direction = 'U'
        
        return reverse_direction

    def find_distance(self, initial_board_str: str, node: str):
        if node == initial_board_str:
            return 0
        return 1 + self.find_distance(initial_board_str, self.graph[node][0][0])
        
    def fill_graph(self, game: Game) -> None:
        # Fill graph with all possible states
        self.graph[game.get_sparse_board()] = [('', ['', ''])]
        
        # initialise
        initial_board = game.get_sparse_board()
        old_games: set[str] = set()
        old_games.add(game.get_sparse_board())
        new_games = set()
        
        # redo this until new_games not empty
        while len(old_games) > 0:
        
            for game_sparse_str in old_games:

                game.set_board_via_sparse_str(game_sparse_str)
                moves_list = self.get_possible_moves(game)
                old_game_str = game.get_sparse_board()
                for move in moves_list:
                    car_name, direction = move
                    game.move(car_name, direction)
                    if game.get_sparse_board() not in self.graph:
                        self.graph[game.get_sparse_board()] = [(old_game_str, (car_name, direction))]
                        new_games.add(game.get_sparse_board())
                    # Dit hieronder hoeft niet: de afstand kan nooit korter worden?
                    #elif (old_game_str, (car_name, direction)) not in self.graph[game.get_sparse_board()]:
                    #    self.graph[game.get_sparse_board()].append((old_game_str, (car_name, direction)))
                        
                    game.move(car_name, self.reverse_direction(direction))
                    
            # dit hieronder wel laten
            old_games = new_games
            new_games = set()
        last_winning_node = ''
        for node in self.graph:
            game.set_board_via_sparse_str(node)
            if game.is_won():
                self.winning_states.append(node)
                last_winning_node = node
                print(self.find_distance(initial_board, self.graph[node][0][0]))
        game.set_board_via_sparse_str(last_winning_node)
        #print(last_winning_node)
        #print('is game won?', game.is_won())
                
        #print(self.winning_states, len(self.winning_states))

