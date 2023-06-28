# Simply script to run multiple instances of solver
import os


def main() -> None:
    """Adjust main to automatically run the desired solvers for given games"""

    # INPUT DATA

    # SPECIFY DESIRED GAMES
    game_numbers = [1, 2, 3, 4, 5, 6, 7]

    # SPECIFY DETERMINISTIC SOLVERS
    deterministic_solver_names = ['breadth_with_storage_parents_solver',
                                  'breadth_with_storage_queue_solver',
                                  'breadth_solver', 'depth_solver',
                                  'count_states']

    # SPECIFY RANDOM SOLVERS AND COUNT
    random_solver_names = ['random_solver', 'random_heur_solver']
    random_solver_count = [5, 5]

    # SPECIFY ASTAR HEURISTICS
    astar_heuristics_choices = ['h0', 'h1', 'h2', 'h3', 'h1h2', 'h1h3']

    # Actual program
    for game_number in game_numbers:
        for solver_name in deterministic_solver_names:
            amount_of_times = 1
            run(game_number, solver_name, amount_of_times)

        for solver_name, amount_of_times in zip(random_solver_names,
                                                random_solver_count):
            run(game_number, solver_name, amount_of_times)

        for heuristics_choice in astar_heuristics_choices:
            solver_name = 'astar_solver'
            amount_of_times = 1
            run_with_heuristics(game_number, solver_name, amount_of_times,
                                heuristics_choice)


def run(game_number: int, solver_name: str, amount_of_times: int) -> None:
    """Run a solver set via name, game number and amount of times"""
    os.system("python3 solver.py " + str(game_number) + " " + solver_name +
              " " + str(amount_of_times) + " 0")


def run_with_heuristics(game_number: int, solver_name: str,
                        amount_of_times: int, heuristics_choice: str) -> None:
    """Run astar solver set via heuristic, game number and amount of times"""
    os.system("python3 solver.py " + str(game_number) + " " + solver_name +
              " " + str(amount_of_times) + " 0 " + heuristics_choice)


if __name__ == '__main__':
    main()
