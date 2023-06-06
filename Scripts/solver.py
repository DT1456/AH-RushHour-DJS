from sys import argv
from game import Game
import time


def get_game_csv_string(game_number: int):
    if game_number not in range(1, 8):
        print('Invalid game_number')
        exit(1)
    
    if game_number in range(1, 4):
        return 'Rushhour6x6_' + str(game_number) + '.csv'
    elif game_number in range(4, 7):
        return 'Rushhour9x9_' + str(game_number) + '.csv'
    else:
        return 'Rushhour12x12_7.csv'


def get_game_dimension(game_number: int):
    if game_number not in range(1, 8):
        print('Invalid game_number')
        exit(1)
    
    if game_number in range(1, 4):
        return 6
    elif game_number in range(4, 7):
        return 9
    else:
        return 12


if __name__ == '__main__':
    
    # Check command line arguments
    if len(argv) not in [4, 5]:
        print("Usage: python3 solver.py game_number solver_script_name amount_of_times [verbose]")
        exit(1)

    # Get game_number, amount_of_times to play and whether to print the board
    game_number, amount_of_times, solver_script_name = int(argv[1]), int(argv[3]), argv[2]
    verbose = (argv[4].upper() == 'TRUE') if len(argv) == 5 else False
    
    # Set solver
    solver_module = __import__(solver_script_name)
    solver = solver_module.Solver()
    
    # Solve
    print('Started solving game ' + str(game_number) + ' for a total of ' + str(amount_of_times) + ' times using solver: ' + solver_script_name + '.py...\n')
    
    start = time.time()
    steps_list = []
    for i in range(amount_of_times):
        g = Game('/home/duco/AH-RushHour-DJS/Input/' + get_game_csv_string(game_number), get_game_dimension(game_number))
      
        if verbose:
            print(g)

        steps = 0
        while not g.is_won():
            g = solver.play_move(g)
            if verbose:
                print(g)
            steps += 1
        steps_list.append(steps)
    
    # Print finished and amount of time passed
    print('Finished in {0:0.1f} seconds'.format(time.time() - start))
    print('----------------------')
    print('Steps statistics:')
    print('Amount of repititions:', amount_of_times)
    print('Average number of steps to solve:', int(sum(steps_list) / len(steps_list)))
    print('Max number of steps to solve:', max(steps_list))
    print('Min number of steps to solve:', min(steps_list))
    
