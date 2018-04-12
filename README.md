# MineSolver
MineSolver is an automated solver of the game Minesweeper on the platform "Minesweeper X".
The aim of the solver is to solve a Minesweeper game with the highest success rate.

What the solver does is trying to solve the game logically and guessing when there is no logical way to solve.
Reinforcement learning technology is used in the solver so that the success rate of guessing can improve by experience.

# How to use
## Download Minesweeper X
Minesweeper X can be downloaded [here](http://www.minesweeper.info/downloads/MinesweeperX.html).
This is only for Windows platform.

## Download Python 3
Python version 3.6 should be downloaded to compile the Minesolver.
In addition, package pywin32 (Python for Windows Extensions) is needed in the solver.
The package can be downloaded by `pip install pywin32` in the cmd.

## Download Minesolver
Download minesolver_v5.py and guess.txt and put them in the same folder.

## Minesweeper X Settings
Download automine.bmp and put it in the same folder with Minesweeper X.
Open Minesweeper X, click "Extras->Custom Skin..." and select automine.bmp.
The automine skin changes each tile into pure color to make it easy to be detected.

## Run Minesolver
Open and run minesolver with Minesweeper X opened.
