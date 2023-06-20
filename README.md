# The Game of Rush Hour
*Sabrina Strijker - Duco Telkamp - Jasmijn Smidt*

<br>

Our project consist of an implementation of the Rush hour game for the course *Algoritmen en Heuristieken*.

## Table of contents

[Directories and files](#directories-and-files)
- [Scripts](#scripts)
- [Solvers](#solvers)
- [Input](#input)

[Instructions](#instructions)
- [Playing the game](#playing-the-game)
- [Using the solver](#using-the-solver)

[Installations](#installations)
- [Terminology (Linux)](#terminology)
- [iTerm2: imgcat (MacOS)](#imgcat)

<br>

## Directories and files

#### **Scripts:** 
This is a directory that contains the python files that together create the game.
- [Game.py:](Scripts/game.py) this file contains the code that brings all the code from the other files together and forms the game.
- [Car.py:](Scripts/car.py) in this file the code for the implementation of the cars in the game is written.
- [Solver.py:](Scripts/solver.py) this file contains the implementation of the code where you can choose what solver you want to apply to the game and how many times you want to solve it.
- [Solvers](Scripts/Solvers) this is the directory with all the different solvers (more information below).

#### **Solvers**:
This directory contains all the solvers that the player can choose from to solve the Rush Hour game:
- [Random_solver.py:](Scripts/Solvers/random_solver.py) this file can solve the Rush Hour game by randomly selecting a car an making random moves with that car.
- [Breadth_solver.py:](Scripts/Solvers/breadth_solver.py) this is the breadth solver, this solver iterates over all the possible options via breadth first search and in the end it chooses the best one (the one with the least steps).
- [Depth_solver.py](Scripts/Solvers/depth_solver.py) after the breadth solver we created the depth solver. This solver iterates over all the possible options via depth first search, when it has found a solution it stops.
- [Astar_solver.py:](Scripts/Solvers/astar_solver.py) this solver... HIER NOG INFO TYPEN!

#### **Input**: 
This directory contains all the different Rush Hour games that the player can choose from.

#### **Legacy**:
In this directory there are some files that we don't use anymore, but they can show some of the process we made. 

<br>

## Instructions

#### **Playing the game**:

If you want to play the game make sure that you run the file **game.py** from the directory that game.py is in. It is also important that every python file is in the same directory. When you want to start the game you have multiple options:

1. **Command line arguments:** if you want to start the game immediately you can choose a game you want from the Input directory and then use the game name in the command line arguments, after python3 game.py you need to type "-f", this means you choose a file for the game:

```python3
    python3 game.py -f Rushhour6x6_1.csv
```

2. **Command line interface:** you can also choose your game through the command line interface. Then you just need to type "python3 game.py". Then you will be asked which board dimension, which game you want to play, if you want to use terminology yes or no and if you want to use imgcat yes or no (see [installations](#installations) for the explanation of terminology and imgcat) after this the game will start.

When the game is ready to be played you can move a car by selecting the letter of the car, typing a space and then the direction (L: left, R: right, U: up or D: down). You proceed like this until you manage to get the red car all the way to the right side of the board. If you succeed you win the game!

<br>

#### **Using the solvers**:

If you want to use the solver, you first need to type "python3 solver.py" in the same line after that you type the number of the game you want to solve (1, 2, 3, 4, 5, 6 or 7), then you type the name of the kind of solver that you want to use, after that you type the amount of times you want to solve the game and then at last there is the option to print the board while solving the game, if you want to print the board you type "True" at the end of the line,if you don't you type nothing there. This would result in something like this:

*When you **don't** want to print:*

    python3 solver.py game_number solver_name amount_of_times

*When you **do** want to print:*

    python3 solver.py game_number solver_name amount_of_times True

#### **Help**:

There is an option to ask for help before you run the game, this is a short summary of what is described above. If you type:

    python3 game.py -h

You get the following output:

![help](/Images/help-function.jpeg)

<br>

## Installations

To make the game visual and see the board with all the cars, installing a terminal that can display pictures is needed. For Linux there is Terminology and for MacOS there is iTerm2 with imgcat. Below there are explanations on how to install these terminals.

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

To install iTerm2 on your Mac you can go to the website "https://iterm2.com" and dowload the terminal from there. Then you can open the terminal as an app on your laptop. When you open the app the left corner in the taskbar says "iTerm2", click on that. A menu pops up and then you need to click "Install Shell Integration". After installing this imgcat will be installed automatically. Imgcat does not work immediatly, you need to close down the iTerm2 terminal and open it up again, then it will work.

To use this terminal as a command line argument when starting the game you need to add "-i" to your command:

```python3
python3 game.py -i
```
