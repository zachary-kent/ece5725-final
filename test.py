import numpy as np
from board import Board
import board

def shift_row_test(expected, input):
    assert list(board.shift_row(np.array(input))) == expected

def test_shift_row():
    shift_row_test(expected=[2, 0, 0, 0], input=[1, 1, 0, 0])
    shift_row_test(expected=[2, 2, 0, 0], input=[1, 1, 1, 1])
    shift_row_test(expected=[2, 0, 0, 0], input=[0, 1, 1, 0])
    shift_row_test(expected=[1, 0, 0, 0], input=[0, 0, 1, 0])
    shift_row_test(expected=[2, 0, 0, 0], input=[1, 0, 1, 0])

b = Board([
    [1, 1, 0, 0],
    [0, 2, 2, 0],
    [1, 0, 3, 3],
    [1, 2, 2, 3]
])
