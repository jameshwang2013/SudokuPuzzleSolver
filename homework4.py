############################################################
# CIS 521: Homework 4
############################################################

student_name = "James Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import defaultdict
import Queue

############################################################
# Section 1: Sudoku
############################################################


def sudoku_cells():
    return [(i, j) for i in xrange(9) for j in xrange(9)]


def sudoku_arcs():
    cells = sudoku_cells()
    # create list of lists by rows, columns, and squares
    rows = [[j for j in cells if j[0] == i] for i in xrange(9)]
    cols = [[j for j in cells if j[1] == i] for i in xrange(9)]
    sqr_ord = iter([i for r in xrange(3, 10, 3)
                   for c in xrange(3, 10, 3)
                   for i in cells
                   if i[0] >= (r - 3) and
                   i[0] < r and
                   i[1] >= (c - 3) and
                   i[1] < c])
    sqr_lst = [[next(sqr_ord) for j in xrange(9)] for i in xrange(9)]
    # create constraint pairs in rows, columns, and squares
    row_pairs = [(j, k) for i in rows for j in i for k in i]
    col_pairs = [(j, k) for i in cols for j in i for k in i]
    sqr_pairs = [(j, k) for i in sqr_lst for j in i for k in i]
    # return unique list of pair constraints
    lst = list(set(row_pairs + col_pairs + sqr_pairs))
    return [i for i in lst if i[0] != i[1]]


def sudoku_rows():
    return [[j for j in sudoku_cells() if j[0] == i] for i in xrange(9)]


def sudoku_cols():
    return [[j for j in sudoku_cells() if j[1] == i] for i in xrange(9)]


def sudoku_sqrs():
    sqrs_order = iter([i for r in xrange(3, 10, 3)
                       for c in xrange(3, 10, 3)
                       for i in sudoku_cells()
                       if i[0] >= (r - 3) and
                       i[0] < r and
                       i[1] >= (c - 3) and
                       i[1] < c])
    return [[next(sqrs_order) for i in xrange(9)] for j in xrange(9)]


def read_board(path):
    with open(path, "r") as file:
        board_vals = [i for i in file.read().splitlines()]
    board_iter = iter("".join(board_vals))
    board_map = defaultdict(str)
    for i in xrange(9):  # rows
        for j in xrange(9):  # columns
            board_map[(i, j)] = next(board_iter)
    v_map = defaultdict(str)
    for i, j in zip(board_map.keys(), board_map.values()):
        if j == "*":
            v_map[i] = set(map(int, range(1, 10))) # change str to int
        else:
            v_map[i] = set(map(int, j)) # change type from str to int
    return v_map


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.map = board
        self.rows = sudoku_rows()
        self.sqrs = sudoku_sqrs()
        self.cols = sudoku_cols()

    def get_values(self, cell):
        return self.map[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        if ((cell1, cell2) in Sudoku.ARCS and
           len(self.get_values(cell2)) == 1):
            keeps = self.get_values(cell1).difference(self.get_values(cell2))
            if keeps:
                if keeps == self.get_values(cell1):
                    self.map[cell1] = keeps
                    return False
                else:
                    self.map[cell1] = keeps
                    return True
        return False

    def infer_ac3(self):
        priority = {i: len(self.map[i]) for i in self.map}
        queue = Queue.PriorityQueue()
        for i in Sudoku.ARCS:
            if len(self.map[i[0]]) != 1:
                queue.put((priority[i[1]], i[0], i[1]))
        while queue.empty() is False:
            p, Xi, Xj = queue.get()
            if self.remove_inconsistent_values(Xi, Xj):
                for Xk in [i for i in Sudoku.ARCS if i[1] == Xi]:
                    queue.put((priority[Xk[1]], Xk[0], Xk[1]))

    def apply_alldiff(self, x, x_domain):
        row_cells = [j for j in [i for i in self.rows if x in i][0] if j != x]
        col_cells = [j for j in [i for i in self.cols if x in i][0] if j != x]
        sqr_cells = [j for j in [i for i in self.sqrs if x in i][0] if j != x]
        row_domain = set(sum([list(self.get_values(k)) for k in row_cells
                              if len(list(self.get_values(k))) > 1], []))
        col_domain = set(sum([list(self.get_values(k)) for k in col_cells
                              if len(list(self.get_values(k))) > 1], []))
        sqr_domain = set(sum([list(self.get_values(k)) for k in sqr_cells
                              if len(list(self.get_values(k))) > 1], []))
        return [i for i in x_domain
                if i not in row_domain or
                i not in col_domain or
                i not in sqr_domain]

    def infer_improved(self):
        self.infer_ac3()
        queue = Queue.Queue()
        for i in [i for i in self.map if len(self.map[i]) > 1]:
            queue.put(i)
        while sum(map(len, [i for i in self.map.values()])) != 81:
            x = queue.get()
            if not queue:
                for i in [i for i in self.map if len(self.map[i]) > 1]:
                    queue.put(i)
            x_domain = self.get_values(x)
            new_domain = self.apply_alldiff(x, x_domain)
            if len(new_domain) > 0:
                self.map[x] = set(new_domain)
                if len(new_domain) == 1:
                    self.infer_ac3()
                else:
                    queue.put(x)
            else:
                queue.put(x)

    def infer_with_guessing(self):
        pass

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
~24 hours Way too long :( Definitely need to use office hours more - but hard
to find time with recruiting going on.
"""

feedback_question_2 = """
I thought the homework difficulty was reasonable.

Hindsight somewhat leaves me at a loss of words because the solutions to the
roadblocks I ran into did not seem very hard - I'm surprised that I did not
find them sooner. I think this hw assignment made me realize a serious flaw in
my programming problem-solving approach: I realize I spend a lot of time doing
trial-and-error instead doing the hard, logical thinking required to breakdown
the problem and come up with a solution. Perhaps this is a bad habit that could
have been addressed had I taken the intro CIS sequence, but alas, I'm glad
I'm realizing it now rather than later.
"""

feedback_question_3 = """
Overall I think Sudoku puzzles are a cool application - I don't think I've ever
done one before, so this exercise was quite fun!
"""
