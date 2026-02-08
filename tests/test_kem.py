from pyber.kem import expand_matrix
from pyber.params import K
from pyber.polynomial import Polynomial


def test_key_key_generation():
    seed = b'test_seed_999999'
    matrix = expand_matrix(seed)
    matrix2 = expand_matrix(seed)

    assert matrix == matrix2
    assert len(matrix) == K
    assert all(len(p) == K for p in matrix)
    assert all(isinstance(p, Polynomial) for vec in matrix for p in vec)


def test_key_key_generation_different_seeds():
    seed1 = b'test_seed_999999'
    seed2 = b'test_seed_999998'
    matrix = expand_matrix(seed1)
    matrix2 = expand_matrix(seed2)
    assert matrix != matrix2
