from dataclasses import dataclass
import pprint
import secrets
from typing import Self
from pyber.encoding import decode_12, decode_polynom, encode_12, encode_polynom, decode_1, encode_1
from pyber.matrix import Matrix, Vec, mat_vec_mul
from pyber.params import K, N, Q
from pyber.polynomial import Polynomial
from pyber.randomness import g_hash_function, generate_noise, h_hash_function
from pyber.compression import compress, decompress

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
    shared_key: bytes
    cypher_text: CyperText

    def serialize(self) -> bytes:
        out = b''
        for poly in self.cypher_text.u:
            out += bytes(encode_polynom(poly))

        out += bytes(encode_polynom(self.cypher_text.v))    
        return out

    @staticmethod
    def unserialize(data: bytes) -> CyperText:
        poly_size = len(data) // (K + 1)
        u = [] 
        for i in range(K):
            start = i*poly_size
            end = start + poly_size
            poly_data = list(data[start:end])
            u.append(decode_polynom(poly_data))
        start = poly_size * K
        end = start + poly_size
        poly_data = list(data[start:end])
        v = decode_polynom(poly_data)
        return CyperText(u, v)
    
transpose_matrix = lambda m: [list(col) for col in zip(*m)]

vec_vec_mul = lambda matrix, scaler: sum([m_i * s_i for m_i, s_i in zip(matrix, scaler)], start=Polynomial.zero())

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
    m = m or secrets.token_bytes(N//8)
    hashed = h_hash_function(pk.serialize())
    k_shared, r = g_hash_function(m + hashed)
    A = expand_matrix(pk.rho)
    r_vec = [Polynomial(generate_noise(r, i)) for i in range(K)]
    e1 = [Polynomial(generate_noise(r, i)) for i in range(K, 2*K)]
    e2 = Polynomial(generate_noise(r, 2*K))

    A_T = transpose_matrix(A)
    clean_u = mat_vec_mul(A_T, r_vec)
    u = [u_part + error1_part for u_part, error1_part in zip(clean_u, e1)]

    v_poly = vec_vec_mul(pk.t, r_vec)
    v_no_message = v_poly + e2
    
    message_bin = decode_1(m)
    message_poly = decompress(message_bin, 1)
    v = v_no_message + Polynomial(message_poly)

    return EncapsulatedKey(shared_key=k_shared, cypher_text=CyperText(u, v))

def decaps(c: CyperText, secret_key: Vec, pk: PublicKey, debug=False) -> bytes:
    s_u_product = vec_vec_mul(secret_key, c.u)
    noisy_m_poly = c.v - s_u_product
    bits = compress(noisy_m_poly.coeffs, 1)
    m_prime = encode_1(bits)

    test_encaps = encapes(pk, m_prime)
    if test_encaps.cypher_text == c:
        return test_encaps.shared_key
    else:
        return None if debug else secrets.token_bytes(32)
