"""
SudokuSolver
by James Matlock
Dec 2020

Provides a solution to a given sudoku as well as
providing an interactive way for users to attempt
a solution with coaching and guidance.

Usage:
    SudokuSolver puzzle.txt [-i]
        puzzle.txt - Input file for sudoku puzzle
        -i Interactive mode (Not yet implemented)

In non-interactive mode, solved sudoku is written to
the console.

This project is still under development. Currently it can read in a
puzzle file, indicate whether the puzzle is completed and/or valid
(to the rules of sudoku), and it will provide hints to the best
starting places to solve the puzzle.
"""
import argparse
import os


def convert_to_dot(val: int):
    if val > 0:
        return str(val)
    else:
        return '.'


class Sudoku:
    def __init__(self):
        self.grid = [0] * 81

    def __str__(self):
        result = ''
        for x in range(0, 81, 9):
            result += ' '.join(map(convert_to_dot, self.grid[x:x + 9])) + '\n'
        return result

    @classmethod
    def sudoku_from_file(cls, filename: str):
        """
        Reads sudoku data from a file and returns a Sudoku instance.
        Format expected is 9 lines of 9 single digits ranging from
        0 to 9. Any 0 is interpreted as an empty square in the sudoku
        puzzle.

        :param filename: sudoku data file

        :return: Sudoku instance
        """
        fromfile = []
        try:
            with open(filename, 'r') as f:
                for row in f:
                    fromfile += list(map(int, row.split(' ')))
        except Exception as e:
            print("File error:", e)
            exit(1)
        result = cls()
        result.grid = list(map(int, fromfile))
        return result

    def is_valid(self):
        """
        Tests if sudoku follows all standard rules for validity,
        specifically, all grid values are unique in their respective
        row, column, and 3x3 square. Note that incomplete sudokus
        (ones containing blanks or 0s) can be valid.
        :return: True if following all standard rules
        """
        for idx in range(len(self.grid)):
            if len(self.candidates(idx)) == 0:
                print(f'Not valid due to position {idx}')
                return False
        return True

    def is_complete(self):
        """
        Tests if sudoku contains no blanks (grid value of 0). Note
        a sudoku can be complete but invalid.

        :return: True if sudoku contains no blanks
        """
        for val in self.grid:
            if val == 0:
                return False
        return True

    def candidates(self, loc):
        """
        Returns a list of all possible valid values for a grid
        location based on uniqueness across row, column, and
        local 3x3 square.

        :param loc: position in sudoku grid (0-80)
        :return: list of valid values
        """
        # print(f'candidate[{loc}]')
        # if value at location is not 0, assume the current value
        # is the only candidate.
        val = self.grid[loc]
        if val != 0:
            # print(f'Location value: {val}')
            return [val]

        results = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        row = loc // 9
        row_set = set(self.grid[row * 9:(row + 1) * 9])
        # print(f'row set = {row_set}')
        col = loc % 9
        col_set = {self.grid[x * 9 + col] for x in range(9)}
        # print(f'col set = {col_set}')
        # for local set, calculate location of upper left square
        upper_left_local = (row // 3 * 27) + (col // 3 * 3)
        local_set = set(self.grid[upper_left_local:upper_left_local+3] +
                        self.grid[upper_left_local+9:upper_left_local+12] +
                        self.grid[upper_left_local+18:upper_left_local+21])
        # print(f'local set = {local_set}')
        results = results - (row_set | col_set | local_set)
        # print(f'results = {results}')
        return list(results)


def sudoku_solve():
    """
    In non-interactive mode, prints the solution to the given
    sudoku.

    In interactive mode, allows the user to guess the solution
    with feedback on correctness

    :return: None
    """
    parser = argparse.ArgumentParser(description='Solve sudoku puzzles')
    parser.add_argument('infile', metavar='str', help='file containing sudoku')
    parser.add_argument('-i', '--interactive', action='store_true', help='interactive mode indicator')
    args = parser.parse_args()

    # print(f'Input file = {args.infile}')
    # print(f'Interactive = {args.interactive}')
    s = Sudoku.sudoku_from_file(args.infile)
    print(s)
    print(f'Complete = {s.is_complete()}')
    print(f'Valid = {s.is_valid()}')
    if s.is_valid():
        for idx in range(len(s.grid)):
            if s.grid[idx] == 0:
                possibles = s.candidates(idx)
                if len(possibles) == 1:
                    print(f'Single candidate at row {idx // 9}, col {idx % 9}')
                elif len(possibles) == 2:
                    print(f'Two candidates at row {idx // 9}, col {idx % 9}')


if __name__ == '__main__':
    sudoku_solve()
