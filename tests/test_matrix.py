from pyber.matrix import mat_vec_mul
from pyber.polynomial import Polynomial

def test_mat_vec_mul_identity():
    one = Polynomial.one()
    zero = Polynomial.zero()
    two = Polynomial.one() * 2

    matrix = [
        [one, zero],
        [zero, one]
    ]

    vec:list[Polynomial] = [one, two]

    result = mat_vec_mul(matrix, vec)

    assert result[0].coeffs == one.coeffs
    assert result[1].coeffs == two.coeffs

def test_mat_vec_mul_swap():
    one = Polynomial.one()
    zero = Polynomial.zero()
    two = Polynomial.one() * 2

    matrix = [
        [zero, one],
        [one, zero]
    ]

    vec:list[Polynomial] = [one, two]

    result = mat_vec_mul(matrix, vec)

    assert result[0].coeffs == two.coeffs
    assert result[1].coeffs == one.coeffs

