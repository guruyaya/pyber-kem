import pytest
from pyber.params import N, Q
from pyber.polynomial import Polynomial

def test_parameters():
    """Test that global parameters are defined correctly for ML-KEM."""
    assert N == 256
    assert Q == 3329

def test_polynomial_initialization():
    """Test basic polynomial initialization and modular reduction."""
    # Test initialization with valid coefficients
    coeffs = [i for i in range(N)]
    poly = Polynomial(coeffs)
    assert len(poly.coeffs) == N
    assert poly.coeffs == coeffs
    
def test_polynomial_modulo_q():
    """Test that coefficients are reduced modulo Q upon initialization."""
    # Create coefficients larger than Q
    input_coeffs = [Q + 5] * N
    expected_coeffs = [5] * N
    
    poly = Polynomial(input_coeffs)
    assert poly.coeffs == expected_coeffs

def test_polynomial_invalid_length():
    """Test that initialization raises error for incorrect number of coefficients."""
    with pytest.raises(ValueError):
        Polynomial([1, 2, 3]) # Too few coefficients

def test_add_polynomial():
    a = Polynomial([num for num in range(256)])
    b = Polynomial([num * 100 for num in range(256)])

    c = a + b
    assert c.coeffs == [(num * 101) % Q for num in range(256)]

def test_sub_polynomial():
    a = Polynomial([num for num in range(256)])
    b = Polynomial([num * 20 for num in range(256)])

    c = a - b
    assert c.coeffs == [(num * -19) % Q for num in range(256)]

def test_mul_polynomial():
    a = Polynomial(([0] * 255) + [1])
    b = Polynomial([0, 1] + ([0] * 254))

    c = a * b
    assert len(c.coeffs) == 256 
    assert c.coeffs == [3328,] + ([0,] * 255)

    d = b * a
    assert c.coeffs == d.coeffs

def test_polynomial_zero():
    a = Polynomial.zero()
    assert all(i == 0 for i in a.coeffs)

def test_polynomial_one():
    a = Polynomial.one()
    assert a.coeffs[0] == 1
    assert all(i == 0 for i in a.coeffs[1:])

def test_polynomial_one_mul():
    a = Polynomial.one() * 2
    assert a.coeffs[0] == 2
    assert all(i == 0 for i in a.coeffs[1:])

