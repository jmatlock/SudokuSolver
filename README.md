# SudokuSolver
Sudoku puzzle solver

**This project is part of a #100DaysOfCode challenge!**

This program will read in a text file that presents a 9x9 Sudoku puzzle. The format should be nine lines
of nine single digits with 0 representing blanks in the puzzle.

In its final version, this program should be able to solve a valid 9x9 Sudoku puzzle using two methods:
* Simple observational rules akin to how a human would solve easier puzzles. At a minimum, it will scan
rows, columns, and local area (local 3x3 in a 9x9) to determine where there are only single candidates possible 
for an empty square. Additional rules may be added as well.
* After using these rules, the program will use a backtracking algorithm to resolve any remaining squares.
* I will implement backtracking using a "dumb" algorithm that disregards number of possible candidates and
one that backtracks on squares with minimum number of candidates first to see changes in performance.
* Command line parameters will be provided to direct program to use different methods.

I also plan to have an interactive version of this program which will allow the user to attempt to solve
the puzzle, and the program will provide feedback on the correctness of the user's guesses. Given the inclusion
of the observational rules, the program should also be able to provide hints to the user as to the best squares
to review which may provide easy progress.

### To be done:
- [x] Read in a sudoku puzzle from a file.
- [x] Determine whether the sudoku is complete (no blanks).
- [x] Determine whether the sudoku is valid (no rule violation).
- [x] Find candidates for each individual square which would not violate rules.
- [x] Step through the puzzle using observational rules and attempt to solve.
- [x] Use backtracking to solve the puzzle.
- [x] Provide timing stats for solving puzzle
- [ ] Use logger for capturing debug and error information
- [x] Provide options for choosing method of solving
- [ ] Provide an interface which will let the user observe the computer solving the puzzle:
    - [x] For naked singles
    - [ ] For other rules
    - [x] For backtracking (not optimized yet)
- [ ] Provide an interactive interface that will allow the user to enter their guesses to complete the puzzle. :construction:
- [ ] Improve performance by storing and updating candidate answers. :construction:
- [ ] Package project using setuptools or equivalent

### Other features to be considered:
- [ ] UI using Tkinter. :construction:
- [ ] Produce "heat map" that shows easiest to most difficult squares to solve. 
- [ ] Provide a grade of the sudoku puzzle in terms of skill level needed by user.
- [ ] Generate a valid Sudoku.
- [ ] Allow for multiple sudokus to be provided in a single file.
- [ ] Allow for variations of grid such as 16x16. :construction:
- [ ] Allow for variations that include other rules like unique diagonals
