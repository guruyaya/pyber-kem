from dataclasses import dataclass
import secrets
from pyber.encoding import encode_polynom
from pyber.matrix import Matrix, Vec, mat_vec_mul
from pyber.params import K, Q
from pyber.polynomial import Polynomial
from pyber.randomness import g_hash_function, generate_noise, h_hash_function
from pyber.compression import decode_1, decompress

@dataclass
class PublicKey:
    t: Vec
    rho: bytes

    def to_tuple(self):
        return self.t,self.rho
    
    def serialize(self) -> bytes:
        out = b''
        for t0 in self.t:
            out += bytes(encode_polynom(t0))
        out += self.rho
        return out

@dataclass
class CyperText:
    u: list[Polynomial]
    v: Polynomial

@dataclass
class EncapsulatedKey:
    shared_key: list[int] # 32 bytes
    cypher_text: CyperText

def expand_matrix(seed: bytes) -> Matrix:
    return [
        [ Polynomial.random_uniform(seed + bytes([j]) + bytes([i])) for j in range(K) ]
            for i in range(K)
    ]

def generate_keys(seed=None) -> tuple[PublicKey, Vec]:
    rho, sigma = g_hash_function(seed)
    A = expand_matrix(rho)
    s = [Polynomial(generate_noise(sigma, i)) for i in range(K)]
    e = [Polynomial(generate_noise(sigma, i+K)) for i in range(K)]
    t = mat_vec_mul(A,s)
    t = [t1+e1 for t1, e1 in zip(t, e, strict=True)]
    return PublicKey(t=t,rho=rho), s

def modular_distance(vec1: Vec, vec2: Vec):
    half_q = Q / 2
    assert len(vec1) == len(vec2)
    
    values = [abs(n1 - n2) for n1, n2 in zip(vec1, vec2)]
    return [v if v < half_q else Q-v for v in values]

def encapes(pk:PublicKey, m: bytes|None=None) -> EncapsulatedKey:
    m = m or secrets.token_bytes(32)
    hashed = h_hash_function(pk.serialize())
    k_shared, r = g_hash_function(m + hashed)
    A = expand_matrix(pk.rho)
    r_vec = [Polynomial(generate_noise(r, i)) for i in range(K)]
    e1 = [Polynomial(generate_noise(r, i)) for i in range(K, 2*K)]
    e2 = Polynomial(generate_noise(r, 2*K))

    A_T = [list(col) for col in zip(*A)]
    clean_u = mat_vec_mul(A_T, r_vec)
    u = [p1 + p2 for p1, p2 in zip(clean_u, e1)]

    v_poly = sum([t_i * r_i for t_i, r_i in zip(pk.t, r_vec)], start=Polynomial.zero())
    v_no_message = v_poly + e2
    
    message_bin = decode_1(m)
    message_poly = decompress(message_bin, 1)
    v = v_no_message + Polynomial(message_poly)

    return EncapsulatedKey(shared_key=k_shared, cypher_text=CyperText(u, v))
