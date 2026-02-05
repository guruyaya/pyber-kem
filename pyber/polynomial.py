from typing import Self
from .params import N, Q
class Polynomial:
    coeffs: list

    def __init__(self, coeffs: list[int]):
        if len(coeffs) != N:
            raise ValueError(f"You've submitted {len(coeffs)}. This function only accepts {N} coefficiants")
        self.coeffs = [c % Q for c in coeffs]

    def __add__(self, other: Self) -> Self:
        return Polynomial([a + b for a, b in zip(self.coeffs, other.coeffs)])

    def __sub__(self, other: Self) -> Self:
        return Polynomial([a - b for a, b in zip(self.coeffs, other.coeffs)])
    
    def _multiply_polinomial(self, other: Self):
        out = [0 for _ in range(N)]
        for i, co1 in enumerate(self.coeffs):
            for j, co2 in enumerate(other.coeffs):
                prod = co1 * co2
                pos = i + j
                if pos < N:
                    out[pos] += prod
                else:
                    out[pos - N] -= prod

        out = [o % Q for o in out]
        return Polynomial(out)
    
    def __mul__(self, other: Self|int) -> Self:
        if isinstance(other, int):
            return Polynomial([cof * other for cof in self.coeffs])
        return self._multiply_polinomial(other=other)
    
    @classmethod
    def zero(cls) -> Self:
        return cls([0] * N)
    
    @classmethod
    def one(cls) -> Self:
        return cls([1] + [0] * (N - 1))
        