from game import Game
from pathlib import Path
from sys import argv
import time


def main() -> None:
    """Main program: run your favorite solver_script on any of the games"""
    # Check command line arguments
    validate_input(argv)

    # Get game_number, amount_of_times to play and the solver_name
    game_number, amount_of_times = int(argv[1]), int(argv[3])
    solver_name = argv[2]

    # Store whether the game should be printed while being solved
    verbose = set_verbose_option(argv)

    # Set solver
    solver_module = __import__(solver_name)
    solver = solver_module.Solver()

    # Welcome the user
    print('Started solving game ' + str(game_number) + ' for a total of ' +
          str(amount_of_times) + ' times using solver: ' + solver_name +
          '.py...\n')

    # Save start_time and initialise steps_list to store the amount of steps
    start_time = time.time()
    steps_list = []

    # Solve the game amount_of_times times
    for _ in range(amount_of_times):
        # Initialise game
        game = Game(get_game_csv_string(game_number),
                    get_game_dimension(game_number))
        print_game(game, verbose)

        # Solve the game, storing the number of steps it took
        steps = 0
        while not game.is_won():
            game = solver.play_move(game)
            steps += 1
            print_game(game, verbose)
            if len(steps_list) > 0 and steps > min(steps_list):
            	break

        # Only store data if game is won. Only print csv if fastest attempt
        if game.is_won():
            game.clean_moves()
            steps_list.append(game.get_step_count())
            if game.get_step_count() == min(steps_list):
            	game.output_to_csv()

    # Print finished and amount of time passed
    print(get_statistics_string(steps_list, amount_of_times, start_time))


def get_game_csv_string(game_number: int) -> str:
    """Based on the game_number, return the name of csv to load"""
    # Any game_number should be in range 1 to 8
    if game_number not in range(1, 8):
        print('Invalid game_number')
        exit(1)

    # Set base_path
    base_path = str(Path(__file__).parent.parent) + '/Input/'

    # Based on game_number, return csv_string
    if game_number in [1, 2, 3]:
        return base_path + 'Rushhour6x6_' + str(game_number) + '.csv'
    elif game_number in [4, 5, 6]:
        return base_path + 'Rushhour9x9_' + str(game_number) + '.csv'
    return base_path + 'Rushhour12x12_7.csv'


def get_game_dimension(game_number: int) -> int:
    """Based on the game_number, return game dimension"""
    # Any game_number should be in range 1 to 8
    if game_number not in [1, 2, 3, 4, 5, 6, 7]:
        print('Invalid game_number')
        exit(1)

    # Based on game_number, return game dimension
    if game_number in [1, 2, 3]:
        return 6
    elif game_number in [4, 5, 6]:
        return 9
    return 12


def print_game(game: Game, verbose: int) -> None:
    """Print the game if verbose is True"""
    if verbose == 2:
        game.set_terminology_print_to_true()
    if verbose in [1, 2]:
        game.show_board()


def validate_input(argv: list[str]) -> None:
    """Validate the CLI input"""
    if len(argv) in [4, 5]:
        return
    show_usage_and_exit()


def show_usage_and_exit() -> None:
    print('Usage: python3 solver.py game_number solver_name amount_of_times '
          '[verbose]\nIf verbose (default = 0) is 0, do not print the board.'
          ' If verbose is 1, print board in ASCII. If verbose is 2, print '
          'board as picture using Terminology.')
    exit(1)


def set_verbose_option(argv: list[str]) -> int:
    """Set the verbose option: determines whether to print game during solve"""
    if len(argv) > 4 and int(argv[4]) not in [0, 1, 2]:
        show_usage_and_exit()
    elif len(argv) > 4:
        return int(argv[4])
    return 0


def get_statistics_string(steps_list: list[int], amount_of_times: int,
                          start_time: float) -> str:
    """Return the statistics in a formatted string to be printed"""
    # Add the time to finish
    statistics_string = 'Finished in {0:0.1f} seconds\n'.format(time.time()
                                                                - start_time)

    # Print step statistics header
    statistics_string += '----------------------\nSteps statistics:\n'
    statistics_string += 'Amount of repititions: {0}\n'.format(amount_of_times)

    # Add average, max and min of steps in steps_list
    statistics_string += 'Average number of steps to solve: {0:0.0f}\n'.format(
        sum(steps_list) / len(steps_list))
    statistics_string += 'Max number of steps to solve: {0}\n'.format(
        max(steps_list))
    statistics_string += 'Min number of steps to solve: {0}\n'.format(
        min(steps_list))
    return statistics_string


if __name__ == '__main__':
    main()
