### TEST FILE ###

'''
TEST Sudoku.get_values()
'''
b = read_board("sudoku/medium1.txt")
B = Sudoku(b)

B.get_values((0, 0)) == set([1, 2, 3, 4, 5, 6, 7, 8, 9])

B.get_values((0, 1)) == set([1])

import pandas as pd
cells_vis = []
idx = 0
for i in range(9):
    cells_vis.append([sudoku_cells()[idx:idx+9]])
    idx += 9
cells_vis


'''
TEST sudoku_arcs
'''
def arcs_tester(i, j):
    return (i, j) in sudoku_arcs()

for i in sudoku_cells():
    for j in sudoku_cells():
        print("Pair: ", (i, j))
        print(arcs_tester(i, j))


'''
TEST remove_inconsistent values
'''

b = read_board("sudoku/easy.txt")

test = Sudoku(b)
test.get_values((0, 1))
for i in sudoku_cells():
    for j in sudoku_cells():
        print("i: ", i, test.get_values(i))
        print("j: ", j, test.get_values(j))
        removed = test.remove_inconsistent_values(i, j)
        print removed, test.get_values(i)

sudoku = Sudoku(read_board("sudoku/easy.txt"))
sudoku.get_values((0, 3))
set([1, 2, 3, 4, 5, 6, 7, 8, 9])
for col in [0, 1, 4]:
    removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
    print sudoku.map[(0, 3)]
    print removed, sudoku.get_values((0, 3))

'''
TEST inf_ac3
'''

test = Sudoku(read_board("sudoku/easy.txt"))
cProfile.run('test.infer_ac3()')
test.map

import time
time1 = time.time()
Sudoku(read_board("sudoku/easy.txt")).infer_ac3()
time.time() - time1

'''
TEST inf_improved
'''

import cProfile
test = Sudoku(read_board("sudoku/medium4.txt"))
cProfile.run('test.infer_improved()')


import time
tests = [Sudoku(read_board("sudoku/medium1.txt")),
         Sudoku(read_board("sudoku/medium2.txt")),
         Sudoku(read_board("sudoku/medium3.txt")),
         Sudoku(read_board("sudoku/medium4.txt"))]

for i in tests:
    time1 = time.time()
    i.infer_improved()
    print((time.time() - time1)/.2)

check = Sudoku(read_board("sudoku/medium4.txt"))
check.infer_improved()
check.map


























