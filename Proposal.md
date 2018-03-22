# COMP7404 Project

Topic: Minesweeper Auto Solver

Group T Members:

CHEN Weizhe 3035029706

LI Qin 3035419511

## Problem

Minesweeper is a classic puzzle game. The goal of the game is to clear a rectangle grid without detonating the mines. The mines are hidden in some of the squares in the grids. When each other safe square is opened, a number indicating the number of mines surrounding itself will appear and provide information to search for mines.

There are three default levels of difficulty: Beginner (9x9 grid with 10 mines), Intermediate (16x16 grid with 40 mines) and Expert (16x30 grid with 99 mines). Our final product will be tested by Expert level game.

## Constraint Satisfaction Problem

The gameplay is essentially continuously solving Constraint Satisfaction Problems (CSP). The following is one typical example:
```
xxx20
1xx20
23210
!1000
```
Numbers are opened safe squares with number of surrounding mines, x are unopened squares and ! are marked mines. Determining whether each unopened square is a mine becomes a sub-CSP.

## Methodology

There are three actions we can take in solving minesweeper.

1. Marking Mines
```
xxC20 
1BA20
23210
!1000
```

For square A, it is the only square to place a mine in order to satisfy the constraint of 1 on the 3rd row. Therefore, it can be marked as mine.

Similar deduction can be applied on B and C, which are also mines to satisfy the constraints of the 2's on the 3rd and 2nd rows. 

So the board becomes the following after marking mines:
```
xx!20 
1!!20
23210
!1000
```

2. Opening Safe Squares
After marking the mines, the constraint of 1 on the 2nd row has been satisfied. Therefore, the remaining two squares and absolutely safe and opened. Then the board becomes the following:

```
24!20 
1!!20
23210
!1000
```

3. Forward Checking
Consider another board as following:
``` 
ABCDE
11211
00000
```
ABCDE are temporarily not opened nor marked. Action 1 and 2 are not applicable so it seems that we can leave it at this moment. However, we can actually come up with a solution with forward checking.

Considering square C is a mine, then the constraint of 1's below B and below D are satisfied and ABDE are marked as safe. However, the constraint of 2 below C is no longer solvable because only 1 mine is found around it. The conclusion is that square C is impossible to be a mine.

After opening C, the constraint of 2 comes to its solution with mines at B and D.
``` 
2!3!1
11211
00000
```

## Demo

Temporarily we have two plans of demo. Plan A is solving on [Minesweeper Online](https://http://minesweeperonline.com/) with Javascript. Plan B is making a Java minesweeper game on our own and solving it.
