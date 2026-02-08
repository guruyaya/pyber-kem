from pyber.kem import expand_matrix, generate_keys
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

def test_key_generation():
    seed = b'The_secret_is_cool_1201119292922'
    public1, secret1 = generate_keys(seed)
    public2, secret2 = generate_keys(seed)

    assert public1 == public2
    print (secret1[0])
    assert secret1 != secret2
    assert len(public1[0]) == K
    assert all(isinstance(p, Polynomial) for p in public1[0])

def test_key_generation_diffrent_seeds():
    seed1 = b'The_secret_is_cool_1201119292922'
    seed2 = b'The_secret_is_uncool_12011192929'
    (pk1, rho1), secret1 = generate_keys(seed1)
    (pk2, rho2), secret2 = generate_keys(seed2)

    assert pk1 != pk2
    assert rho1 != rho2
    assert secret1 != secret2
