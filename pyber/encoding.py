from pyber.params import Q
from pyber.polynomial import Polynomial
from more_itertools import windowed

def encode_12(num1: int, num2: int) -> tuple[int, int, int]:
    MAX_12_BITS = 0b111_111_111_111
    assert num1 <= MAX_12_BITS
    assert num2 <= MAX_12_BITS
        
    out1 = num1 & 0xFF
    out2 = ((num1 >> 8) | (num2 << 4)) & 0xFF
    out3 = (num2 >> 4) & 0xFF

    return out1, out2, out3

def decode_12(num1:int, num2:int, num3:int) -> tuple[int, int]:
    MAX_8_BITS = 255
    assert num1 <= MAX_8_BITS
    assert num2 <= MAX_8_BITS
    assert num3 <= MAX_8_BITS

    out1 = num1
    out1 += (num2 & 0xF) << 8
    out2 = num3 << 4
    out2 += num2 >> 4
    return out1, out2

def encode_polynom(polynom: Polynomial) -> list[int]:
    coeffs = polynom.coeffs
    out = []
    for num1, num2 in windowed(coeffs, 2, step=2):
        out += list(encode_12(num1, num2))
    
    return out