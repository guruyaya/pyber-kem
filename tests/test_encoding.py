import pytest
from pyber.encoding import encode_12, decode_12, encode_polynom
from pyber.params import N
from pyber.polynomial import Polynomial


def test_encode_12():
    num1=0b1111_1111_1110
    num2=0b1000_0000_0001

    out1, out2, out3 = encode_12(num1, num2)
    assert out1 == 0b1111_1110
    assert out2 == 0b0001_1111
    assert out3 == 0b1000_0000

def test_encode_12_large_numbers():
    num1=0b1_111_111_111_110
    num2=0b111_111_111_110
    
    with pytest.raises(AssertionError):
        encode_12(num1, num2)
    
    with pytest.raises(AssertionError):
        encode_12(num2, num1)
    
def test_decode_12():
    num1 = 0b1111_1110
    num2 = 0b0001_1111
    num3 = 0b1000_0000

    out1, out2 = decode_12(num1, num2, num3)

    assert out1 == 0b1111_1111_1110
    assert out2 == 0b1000_0000_0001

def test_decode_12_large_numbers():
    num1 = 256
    num2 = 30
    num3 = 255

    with pytest.raises(AssertionError):
        decode_12(num1, num2, num3)

    with pytest.raises(AssertionError):
        decode_12(num2, num3, num1)

    with pytest.raises(AssertionError):
        decode_12(num3, num1, num2)

def test_encode_polynom():
    polynom = Polynomial(list(range(N)))

    encoded = encode_polynom(polynom)
    assert len(encoded) == (N * 3) / 2