from pyber.params import Q

def compress(x: list[int], d:int) -> list[int]:
    inner = lambda n: ((n * (2**d) + (Q // 2)) // Q) % (2**d)
    return [inner(n) for n in x]

def decompress(y: list[int], d:int) -> list[int]:
    inner = lambda n: (n * Q + (2**(d-1))) // (2**d) % Q
    return [inner(n) for n in y]

def decode_1(byte_list: bytes) -> list[int]:
    out = []
    for byte in byte_list:
        for i in range(8):
            out.append(int((byte >> i) & 1))
    return out
