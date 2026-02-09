import pytest
from pyber.kem import expand_matrix, generate_keys, modular_distance
from pyber.matrix import mat_vec_mul
from pyber.params import ETA, K, Q
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

def test_key_generation():
    seed = b'The_secret_is_cool_2201119292934'
    (t1, rho1), secret1 = generate_keys(seed)
    (t2, rho2), secret2 = generate_keys(seed)

    assert t1 == t2
    assert rho1 == rho2
    assert secret1 == secret2
    assert len(t1) == K
    assert len(secret1) == K
    A = expand_matrix(rho1)
    assert len(A) == K
    for calculated_secret, error_bound_secret in zip(mat_vec_mul(A, secret1), t1):
        assert all(num <= ETA for num in modular_distance(calculated_secret, error_bound_secret))
    assert all(isinstance(p, Polynomial) for p in t1)

def test_key_generation_diffrent_seeds():
    seed1 = b'The_secret_is_cool_1201119292922'
    seed2 = b'The_secret_is_uncool_12011192929'
    (pk1, rho1), secret1 = generate_keys(seed1)
    (pk2, rho2), secret2 = generate_keys(seed2)

    assert pk1 != pk2
    assert rho1 != rho2
    assert secret1 != secret2

def test_modular_distance():
    with pytest.raises(AssertionError):
        modular_distance([0, 1, Q -1], [0, Q-1])
    mod_dist = modular_distance([0, 1, Q -1], [0, Q-1, 1])
    assert all(num >= 0 for num in mod_dist)
    assert all([num <= ETA for num in mod_dist])
