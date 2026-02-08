from .polynomial import Polynomial
from functools import reduce

Vec = list[Polynomial]
Matrix = list[Vec]
def mat_vec_mul(matrix:Matrix, vec: Vec) -> list[Polynomial]:
    if len (vec) != len(matrix):
        raise ValueError("Both polynomial and vector have to have the same size")
    out = []
    for matrix_line in matrix:
        to_sum = [mat_item * vec_item for vec_item, mat_item in zip(matrix_line, vec)]
        _sum = reduce(lambda item1, item2: item1 + item2, to_sum)
        out.append(_sum)
    return out