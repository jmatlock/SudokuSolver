# SudokuSolver
Sudoku puzzle solver

**This project is part of a #100DaysOfCode challenge!**

This program will read in a text file that presents a 9x9 Sudoku puzzle. The format should be nine lines
of nine single digits with 0 representing blanks in the puzzle.

In its final version, this program should be able to solve a valid 9x9 Sudoku puzzle using two methods:
* Simple observational rules akin to how a human would solve easier puzzles. At a minimum, it will scan
rows, columns, and local 3x3s to determine where there are only single candidates possible for an empty
sqare. Additional rules may be added as well.
* After using these rules, the program will use a backtracking algorithm to resolve any remaining squares.

I also plan to have an interactive version of this program which will allow the user to attempt to solve
the puzzle, and the program will provide feedback on the correctness of the user's guesses. Given the inclusion
of the observational rules, the program should also be able to provide hints to the user as to the best squares
to review which may provide easy progress.

### To be done:
- [x] Read in a sudoku puzzle from a file.
- [x] Determine whether the sudoku is complete (no blanks).
- [x] Determine whether the sudoku is valid (no rule violation).
- [x] Find candidates for each individual square which would not violate rules.
- [ ] Step through the puzzle using observational rules and attempt to solve.
- [ ] Use backtracking to solve the puzzle.
- [ ] Provide an interface which will let the user observe the computer solving the puzzle
- [ ] Provide an interactive interface that will allow the user to enter their guesses to complete the puzzle.
- [ ] Improve performance by storing and updating candidate answers.

### Other features to be considered:
- [ ] UI using Tkinter.
- [ ] Provide a grade of the sudoku puzzle in terms of skill level needed by user.
- [ ] Generate a valid Sudoku.
- [ ] Allow for multiple sudokus to be provided in a single file.
- [ ] Allow for variations of grid such as 16x16.
- [ ] Allow for variations that include other rules like unique diagonals
