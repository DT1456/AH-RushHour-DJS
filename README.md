# The Game of Rush Hour
*Sabrina Strijker - Duco Telkamp - Jasmijn Smidt*

<br>

Our project consist of an implementation of the Rush hour game for the course *Algoritmen en Heuristieken*.

## Table of contents

[Directories and files](#directories-and-files)
- [Scripts](#scripts)
- [input](#input)

[Instructions](#instructions)
- [Playing the game](#playing-the-game)
- [Using the solver](#using-the-solver)

<br>

## Directories and files

#### **Scripts:** 
this is a directory that contains the python files that together create the game.
- [Game.py:](Scripts/game.py) this file contains the code that brings all the code from the other files together and forms the game.
- [Car.py:](Scripts/car.py) in this file the code for the implementation of the cars in the game is written.
- [Random_solver.py:](Scripts/random_solver.py) this file can solve the Rush Hour game by randomly selecting a car an making random moves with that car.
- [Solver.py:](Scripts/solver.py) this file contains the implementation of the code where you can choose what solver you want to apply to the game and how many times you want to solve this.
- [Board_visual.py](Scripts/board_visual.py) this file consist of the code that makes the game more visual and easier to play.

#### **Input**: 
this directory contains all the different Rush Hour games that the player can choose from.

<br>

## Instructions

#### **Playing the game**:

If you want to play the game make sure that you run the file **game.py** from the directory that game.py is in. It is also important that every python file is in the same directory. When you want to start the game you have multiple options:

1. **Command line arguments:** if you want to start the game immediately you can choose a game you want from the Input directory and then use the game name in the command line arguments, after python3 game.py you need to type "-f", this means you choose a file for the game:

```python3
    python3 game.py -f Rushhour6x6_1.csv
```

2. **Command line interface:** you can also choose your game through the command line interface. Then you just need to type "python3 game.py". Then you will be asked which board dimension and which game you want to play and then the game will start.

When the game is ready to be played you can move a car by selecting the letter of the car, typing a space and then the direction (L: left, R: right, U: up or D: down). You proceed like this until you manage to get the red car all the way to the right side of the board. If you succeed you win the game!

<br>

#### **Using the solver**:

If you want to use the solver, you first need to type "python3 solver.py" in the same line after that you type the number of the game you want to solve (1, 2, 3, 4, 5, 6 or 7), then you type the name of the kind of solver that you want to use, after that you type the amount of times you want to solve the game and then at last there is the option to print the board while solving the game, if you want to print the board you type "True" at the end of the line,if you don't you type nothing there. This would result in something like this:

*When you **don't** want to print:*

    python3 solver.py game_number solver_name amount_of_times

*When you **do** want to print:*

    python3 solver.py game_number solver_name amount_of_times True

#### Help:

There is an option to ask for help before you run the game, this is a short summary of what is described above. If you type:

    python3 game.py -h

You get the following output:

![help](/Images/help-function.jpeg)