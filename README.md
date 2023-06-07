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

If you want to play the game make sure that you run the file **game.py** from the directory that game.py is in. It is also important that every python file is in the same directory. When you want to start the game you type "python3 game.py". Then you will be asked which board dimension you want and after that which game with that dimension you want to play. When the game is ready to be played you can move a car by selecting the letter of the car, typing a space and then the direction (L: left, R: right, U: up or D: down). You proceed like this until you manage to get the red car all the way to the right side of the board. If you succeed you win the game!

#### **Using the solver**:


