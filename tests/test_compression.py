import logging
from pyber.compression import compress, decompress
from pyber.params import Q


def test_compression():
    d = 4
    d_exponent = 2**d
    x = list(range(Q))
    compressed = compress(x, d)

    find_every = Q // d_exponent
    first_pos = find_every // 2
    for i in range(d_exponent - 1):
        assert compressed[first_pos + (i * find_every)] == i

def test_decompression():
    d = 4
    d_exponent = 2**d
    x = list(range(Q))
    compressed = compress(x, d)
    y = decompress(compressed, d)
    half_step = Q / d_exponent // 2
    for i, (x1, y1) in enumerate(zip(x, y)):
        assert abs(x1 - y1) % Q <= half_step or (y1 == 0 and x1 >= (Q - half_step)), f"Failed on step {i}"