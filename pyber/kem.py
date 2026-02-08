from pyber.matrix import Matrix, Vec, mat_vec_mul
from pyber.params import K
from pyber.polynomial import Polynomial
from pyber.randomness import g_hash_function, generate_noise


def expand_matrix(seed: bytes) -> Matrix:
    return [
        [ Polynomial.random_uniform(seed + bytes([j]) + bytes([i])) for j in range(K) ]
            for i in range(K)
    ]

def generate_keys(seed=None) -> tuple[tuple[Vec, bytes], Vec]:
    rho, sigma = g_hash_function(seed)
    A = expand_matrix(rho)
    s = [Polynomial(generate_noise(sigma, i)) for i in range(K)]
    e = [Polynomial(generate_noise(sigma, i+K)) for i in range(K)]
    t = mat_vec_mul(A,s)
    t = [t1+e1 for t1, e1 in zip(t, e, strict=True)]
    return (t,rho), s