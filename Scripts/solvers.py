# Simply script to run multiple instances of solver
import os
import solver


def run(game_number: int, solver_name: str, amount_of_times: int):
    os.system("python3 solver.py " + str(game_number) + " " + str(solver_name) + " " + str(amount_of_times) + " 0")


if __name__ == '__main__':
    for game_number in [1, 2, 3, 5]:
        solver_name = 'breadth_with_storage_parents_solver'
        amount_of_times = 1
        run(game_number, solver_name, amount_of_times)
