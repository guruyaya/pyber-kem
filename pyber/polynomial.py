from typing import Self
from .params import N, Q
from .randomness import generate_uniform, generate_noise
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
    
    def _multiply_polynomial(self, other: Self):
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
        return self._multiply_polynomial(other=other)
    
    def __eq__(self, value: Self):
        return len(self.coeffs) == len(value.coeffs) and all(a == b for a, b in zip(self.coeffs, value.coeffs))
    
    @classmethod
    def zero(cls) -> Self:
        return cls([0] * N)
    
    @classmethod
    def one(cls) -> Self:
        return cls([1] + [0] * (N - 1))
    
    @classmethod
    def random_uniform(cls, seed) -> Self:
        return cls(generate_uniform(seed))

    @classmethod
    def random_noise(cls, seed, nonce) -> Self:
        return cls(generate_noise(seed, nonce))
        
    def __str__(self):
        return f"<Polynomial ({self.coeffs})>"
        
    def __iter__(self) -> iter:
        return iter(self.coeffs)
    
    def __len__(self) -> int:
        return len(self.coeffs)