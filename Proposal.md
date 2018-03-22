# COMP7404 Project

Topic: Minesweeper Auto Solver
Group T Members:
CHEN Weizhe 3035029706
Li Qin

## Problem

Minesweeper is a classic puzzle game. The goal of the game is to clear a rectangle grid without detonating the mines. The mines are hidden in some of the squares in the grids. When each other safe square is opened, a number indicating the number of mines surrounding itself will appear and provide information to search for mines.

There are three default levels of difficulty: Beginner (9x9 grid with 10 mines), Intermediate (16x16 grid with 40 mines) and Expert (16x30 grid with 99 mines). Our final product will be tested by Expert level game.

## Constraint Satisfying Problem

The gameplay is essentially continuously solving Constraint Satisfying Problems (CSP). There will be mainly three kinds of CSP in the game:

