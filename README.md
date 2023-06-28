# The Game of Rush Hour
*Sabrina Strijker - Duco Telkamp - Jasmijn Smidt*

<br>

Our project consists of an implementation of the Rush hour game for the course *Algoritmen en Heuristieken*.

## Table of contents

[What is our problem?](#what-is-our-problem)
- [The case](#the-case)
- [How to play the game?](#how-to-play-the-game)
- [Statespace](#statespace)

[Directories and files](#directories-and-files)
- [Scripts](#scripts)
- [Solvers](#solvers)
- [Input](#input)

[Instructions](#instructions)
- [Using the solver](#using-the-solvers)

[Optional installations](#optional-installations)
- [Terminology (Linux)](#terminology)
- [iTerm2: imgcat (MacOS)](#iterm2---imgcat)

<br>

## What is our problem?

#### **The case:**

Our case is about the game Rush Hour. The goal is to release the red car from the board, to make this possible the cars that are in the way need to be moved Cars can only move horizontically or vertically depending on their orientation. Furthermore, the cars cannot pass over eachother.

![rushhour](/Images/rushhour-board.png)

>Visual representation of the board

#### **How to play the game?**

To play the game run **game.py**. before starting the game you have multiple options:

1. **Board dimension:** You choose the board dimension of your game.
2. **Which game?** You can choose a game number.
3. **Visualisation:** You can choose if you want a visualisation of the board (see [optional installations](#optional-installations) for the explanation of terminology and imgcat) after this the game will start.

When the game is ready to be played you can move a car in two ways:

- *1 or -1:* when you type '-1' the car wil move left or upwards, when you type '1' the car will move right or downwards.
- *U, D, L, R:* 'U' stands for 'up', 'D' stands for 'down', 'L' stands for left and 'R' stands for 'right'.

The line in the command line interface will look as follows (in this example car A moves to the left):

    A -1

Or:

    A L

It does not matter if you type in upper or lowercase, the game accepts both.
You proceed like this until you manage to get the red car all the way to the right side of the board. If you succeed you win the game!

<br>

#### **Statespace:**


Statespace reflects the size of our problem, this table below consists of the maximum number of board states our play boards can reach. This is calculated by taking the product of all the possible board states for every row and column per board.

| Board number | Statespace |
|    :---      |    :---:   |
| Board 1 6x6  | 2025000    |
| Board 2 6x6  | 13500000   |
| Board 3 6x6  | 1000000    |
| Board 4 9x9  | 6.78E+12   |
| Board 5 9x9  | 1.87E+17   |
| Board 6 9x9  | 1.36E+18   |
| Board 7 12x12| 1.20E+30   |

> Calculations can be made available upon request.

<br>

## Directories and files

#### **Scripts:** 
This is a directory that contains the python files that together create the game.
- [Game.py:](Scripts/game.py) this file contains the code that brings all the code from the other files together and forms the game.
- [Car.py:](Scripts/car.py) in this file the code for the implementation of the cars in the game is written.
- [Solver.py:](Scripts/solver.py) this file contains the implementation of the code where you can choose what solver you want to apply to the game and how many times you want to solve it.
- [Solvers](Scripts/Solvers) this is the directory with all the different solvers (more information below).

#### **Results:**
This directory contains all the results that we have runned. Each game has it's own folder and there is a folder that contains the best solution of each game (the solution with the least amount of steps). This does not contain game 6 and 7, because the best result could not be found (these games exceeded the maximum memory of our computers). In each folder there are results of the game with different algorithms. An example:

    3,1,breadth_solver.txt

The '3' stands for the game, the '1' for the number of times we runned the algorithm and 'breadth_solver' stands for the name of the algorithm.

#### **Solvers**:
This directory contains all the solvers that the player can choose from to solve the Rush Hour game:
- [Random_solver.py:](Scripts/Solvers/random_solver.py) this file can solve the Rush Hour game by randomly selecting a car and making random moves with that car.
- [Random_heur_solver.py:](/Scripts/Solvers/random_heur_solver.py) this solver checks if the solution is worse than the solution before, if yes it stops and starts again until it finds a better solution, it also checks if a state has been visited yet, so it won't visit that state again (except no other state is possible).
- [Breadth_solver.py:](Scripts/Solvers/breadth_solver.py) this is the breadth first search solver, this solver iterates over all the possible options via breadth first search and, in the end, it chooses the best solution (the one with the least steps).
- [Depth_solver.py:](Scripts/Solvers/depth_solver.py) This is the depth first search solver, it iterates over all the possible options via depth first search, when it has found a solution it stops.
- [Astar_solver.py:](Scripts/Solvers/astar_solver.py) this A* solver is a best-first search which uses heuristics to search the most promising paths first. We used four different heuristics and combinations of those. All heuristics are admissable: hence guaranteeing the shortest path.
    - H0: Dijkstra algorithm.
    - H1: takes into account the distance from the red car to the exit.
    - H2: takes into account the number of cars between the red car and the exit.
    - H3: takes into account the number of cars between the red car and the exit, but also takes into account if those cars are blocked or not.

#### **Input**: 
This directory contains all the different Rush Hour games that the player can choose from.

<br>

## Instructions

#### **Using the solvers**:

If you want to use the solver, you first need to type "python3 solver.py", next you type the number of the game you want to solve (1, 2, 3, 4, 5, 6 or 7), then you type the name of the kind of solver that you want to use, after that you type the amount of times you want to solve the game and at last there is the option to print the boardstring or the visual board while solving the game. If you want to print the boardstring you type "1" at the end of the line, if you don't you type "0" instead and when you want to see the visual board you type "2". This would result in something like this:

*When you **don't** want to print:*

    python3 solver.py game_number solver_name amount_of_times 0

*When you **do** want to print (boardstring):*

    python3 solver.py game_number solver_name amount_of_times 1

*When you **do** want to print (visual board):*

    python3 solver.py game_number solver_name amount_of_times 2

#### **Help**:

There is an option to ask for help before you run the game, this is a short summary of what is described above. If you type:

    python3 game.py -h

You get the following output:

![help](/Images/help-function2.jpeg)

<br>

## Optional installations

There is the option to make the game visual and see the board with all the cars. Then installing a terminal that can display pictures is needed. For Linux there is Terminology and for MacOS there is iTerm2 with imgcat. Below there are explanations on how to install these terminals.

<br>

#### **Terminology:**

To install Terminology you type in this line in your current terminal:

```python3
sudo apt-get install terminology
```

After installing this you can open Terminology by typing in "terminology" in your terminal.
Then a new terminal will be opened that you can use like your normal terminal, but in here the option to display images is possible.

To use this as a command line argument when starting the game you need to add "-t" to your command:

```python3
python3 game.py -t
```

<br>

#### **iTerm2 -> imgcat:**

To install iTerm2 on your Mac you can go to the website "https://iterm2.com" and dowload the terminal from there. Then you can open the terminal as an app on your laptop. When you open the app the left corner in the taskbar says "iTerm2", click on this. A menu pops up and then you need to click "Install Shell Integration". After installing this imgcat will be installed automatically. Imgcat does not work immediatly, you need to close down the iTerm2 terminal and open it up again, then it will work.

To use this terminal as a command line argument when starting the game you need to add "-i" to your command:

```python3
python3 game.py -i
```
