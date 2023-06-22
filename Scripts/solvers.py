# Simply script to run multiple instances of solver
import os
import solver


def run(game_number: int, solver_name: str, amount_of_times: int):
    os.system("python3 solver.py " + str(game_number) + " " + str(solver_name) + " " + str(amount_of_times) + " 0")


if __name__ == '__main__':
    game_number = 1
    solver_name = 'random_solver'
    amount_of_times = 10
    run(game_number, solver_name, amount_of_times)
