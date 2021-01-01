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
from Timer import Timer
import copy
import tkinter as tk
import time


class Display:
    def __init__(self):
        self.answer_cells = []
        self.display = None
        self.button = None
        self.sudoku = None

    def setup_display(self, infile: str, s):
        self.sudoku = s
        self.display = tk.Tk()
        self.display.title(infile)
        self.display.columnconfigure(0, weight=1, minsize=40)
        self.display.rowconfigure(0, weight=1, minsize=40)
        playfield = tk.Frame(master=self.display,
                             relief=tk.SUNKEN,
                             borderwidth=1)
        playfield.grid(row=0, column=0)

        for row in range(s.rows):
            playfield.columnconfigure(row, weight=1, minsize=40)
            playfield.rowconfigure(row, weight=1, minsize=40)
            for col in range(s.cols):
                frame = tk.Frame(master=playfield,
                                 relief=tk.RAISED,
                                 borderwidth=1)
                frame.grid(row=row, column=col, sticky='nsew')
                val = str(s.grid[row * s.cols + col])
                if val == "0":
                    val = "."
                label = tk.Label(master=frame, text=f"{val}")
                self.answer_cells.append(label)
                label.pack(padx=5, pady=5)

        buttonfield = tk.Frame(master=self.display, pady=10)
        buttonfield.grid(row=1, column=0)
        button1 = tk.Button(master=buttonfield,
                            pady=10,
                            text="Solve it",
                            command=self.animate_solution)
        self.button = button1
        button1.pack()

    def event_loop(self):
        self.display.mainloop()

    def animate_solution(self):
        updated_cell = self.sudoku.solve_naked_single_one_step()
        while updated_cell is not None:
            self.answer_cells[updated_cell]["text"] = f"{self.sudoku.grid[updated_cell]}"
            self.answer_cells[updated_cell].update()
            # print(f'Cell {updated_cell} updated with value {self.sudoku.grid[updated_cell]}')
            time.sleep(0.25)
            updated_cell = self.sudoku.solve_naked_single_one_step()
        self.button["text"] = "Operation Complete"
        self.button["command"] = self.display.quit


def convert_to_dot(val: int):
    if val > 0:
        return str(val)
    else:
        return '.'


class Sudoku:
    def __init__(self):
        # By default we assume the classic 9x9 Sudoku.
        self.rows = 9
        self.cols = 9
        self.values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.grid = [0] * (self.rows * self.cols)
        self.candidates = [[]] * (self.rows * self.cols)

    def __str__(self):
        result = ''
        for x in range(0, (self.rows * self.cols), self.rows):
            result += ' '.join(map(convert_to_dot, self.grid[x:x + self.cols])) + '\n'
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
                    # Enable commenting with hashtag in first column
                    if row[0] != '#':
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
            if len(self.possibles(idx)) == 0:
                # print(f'Not valid due to position {idx}')
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

    def possibles(self, loc):
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
            self.candidates[loc] = [val]
            return [val]

        results = self.values
        row = loc // self.cols
        row_set = set(self.grid[row * self.cols:(row + 1) * self.cols])
        # print(f'row set = {row_set}')
        col = loc % self.cols
        col_set = {self.grid[x * self.rows + col] for x in range(self.rows)}
        # print(f'col set = {col_set}')
        # for local set, calculate location of upper left square
        # TODO: Parameterize the hardcoded values for local set determination
        upper_left_local = (row // 3 * 27) + (col // 3 * 3)
        local_set = set(self.grid[upper_left_local:upper_left_local + 3] +
                        self.grid[upper_left_local + 9:upper_left_local + 12] +
                        self.grid[upper_left_local + 18:upper_left_local + 21])
        # print(f'local set = {local_set}')
        results = results - (row_set | col_set | local_set)
        # print(f'results = {results}')
        self.candidates[loc] = list(results)
        return list(results)

    def solve_naked_singles(self):
        s_answer = copy.deepcopy(self)
        one_to_solve = True
        iterations = 0
        while one_to_solve:
            one_to_solve = False
            if s_answer.is_valid() and not s_answer.is_complete():
                iterations += 1
                for idx in range(len(s_answer.grid)):
                    if s_answer.grid[idx] == 0:
                        possibles = s_answer.candidates[idx]
                        if len(possibles) == 1:
                            s_answer.grid[idx] = possibles[0]
                            one_to_solve = True
        return s_answer, iterations

    def solve_naked_single_one_step(self):
        """
        Solves one square in Sudoku using naked single rule.

        :return: Index of updated square or None if invalid or complete
        """
        if self.is_valid() and not self.is_complete():
            for idx in range(len(self.grid)):
                if self.grid[idx] == 0:
                    possibles = self.candidates[idx]
                    if len(possibles) == 1:
                        self.grid[idx] = possibles[0]
                        return idx
        else:
            return None

    def solve_backtracking_not_optimized(self):
        print('Starting backtrack: ')
        solution = copy.deepcopy(self)

        def extend_solution(position):
            # print(f'{position} ', end='')
            if position >= len(solution.grid):
                print()
                return solution
            if solution.grid[position] != 0:
                return extend_solution(position+1)
            else:
                for possible in solution.possibles(position):
                    # print(f'trying {possible} in position {position}')
                    solution.grid[position] = possible
                    if not solution.is_valid():
                        # print(f'{solution}')
                        solution.grid[position] = 0
                        continue
                    elif extend_solution(position+1) is not None:
                        # print()
                        return solution
            solution.grid[position] = 0
            # print('Backtrack')
            return None

        return extend_solution(0)

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
    parser.add_argument('-b', '--backtrack', action='store_true', help='solve via backtracking')
    args = parser.parse_args()

    # print(f'Input file = {args.infile}')
    # print(f'Interactive = {args.interactive}')
    s = Sudoku.sudoku_from_file(args.infile)
    if not args.interactive:
        print(f'Puzzle from {args.infile}\n')
        print(s)
    else:
        d = Display()
        s_prime = copy.deepcopy(s)
        d.setup_display(args.infile, s_prime)
        d.event_loop()

    if args.backtrack:
        with Timer("Backtracking Not Optimized", text="Backtrack: {:0.4f} seconds"):
            solution = s.solve_backtracking_not_optimized()
        if solution is not None:
            print(f'Solution via backtracking\n{solution}')
        else:
            print('Solution not found via backtracking')

    print(f'Complete = {s.is_complete()}')
    print(f'Valid = {s.is_valid()}')

    with Timer("Solving naked single only", text="Solving time (naked single only): {:0.4f} seconds"):
        s_answer, iterations = s.solve_naked_singles()
    print(f'Answer via naked singles method:\n{s_answer}')
    if s_answer.is_complete():
        print(f'Sudoku solved in {iterations} iterations')
    else:
        unsolved = [x for x in s_answer.candidates if len(x) > 0]
        print(f'Sudoku not solved in {iterations} iterations. {len(unsolved)} remaining squares.')



if __name__ == '__main__':
    sudoku_solve()
