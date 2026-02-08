from pyber.matrix import Matrix
from pyber.params import K
from pyber.polynomial import Polynomial


def expand_matrix(seed: bytes) -> Matrix:
    return [
        [ Polynomial.random_uniform(seed + bytes([j]) + bytes([i])) for j in range(K) ]
            for i in range(K)
    ]