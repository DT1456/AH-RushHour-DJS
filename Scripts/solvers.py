# Simply script to run multiple instances of solver
import os
import solver


def main():
    for game_number in [1, 2, 3]:
        solver_name = 'breadth_with_storage_parents_solver'
        amount_of_times = 1
        run(game_number, solver_name, amount_of_times)
        
        solver_name = 'breadth_with_storage_queue_solver'
        amount_of_times = 1
        run(game_number, solver_name, amount_of_times)
        
        solver_name = 'breadth_solver'
        amount_of_times = 1
        run(game_number, solver_name, amount_of_times)
        
        solver_name = 'depth_solver'
        amount_of_times = 1
        run(game_number, solver_name, amount_of_times)
        
        for heuristics_choice in ['h0', 'h1', 'h2', 'h3', 'h1h2', 'h1h3']:
            solver_name = 'astar_solver'
            amount_of_times = 1
            run_with_heuristics(game_number, solver_name, amount_of_times, heuristics_choice)
            
        solver_name = 'count_states'
        amount_of_times = 1
        run(game_number, solver_name, amount_of_times)


def run(game_number: int, solver_name: str, amount_of_times: int):
    os.system("python3 solver.py " + str(game_number) + " " + solver_name + " " + str(amount_of_times) + " 0")
    

def run_with_heuristics(game_number: int, solver_name: str, amount_of_times: int, heuristics_choice: str):
    os.system("python3 solver.py " + str(game_number) + " " + solver_name + " " + str(amount_of_times) + " 0 " + heuristics_choice)


if __name__ == '__main__':
    main()
