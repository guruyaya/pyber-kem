from hashlib import sha3_256, shake_128, shake_256, sha3_512
import secrets
from pyber.params import ETA, N, Q

first_number_mask = int("0" * 12 + "1"*12, 2)

def get_2_numbers(provided_bytes: bytes) -> tuple[int, int]:
    total_number = int.from_bytes(provided_bytes, byteorder='little')
    first = total_number & first_number_mask
    second = total_number >> 12
    return (first, second)

def generate_uniform(seed: bytes) -> list[int]:
    coeffs = []
    xof = shake_128(seed)
    provided_bytes = xof.digest(50400) # 168 * 3
    for i in range(16800):
        bits_24 = provided_bytes[i*3:i*3+3]
        for num in get_2_numbers(bits_24):
            if num < Q:
                coeffs.append(num)
            if len(coeffs) >= N:
                return coeffs
    raise Exception("This is taking too long, just get another seed")

def generate_noise(seed: bytes, nonce: int, eta: int = 2) -> list[int]:
    if eta != 2:
        raise NotImplementedError("For learning purposes, let's start with ETA=2")
        
    coeffs = []
    # 1. PRF: Prepare input (Seed + Nonce)
    # nonce.to_bytes(1, 'little') is safer than bytes([nonce]) for larger numbers, 
    # but for Kyber nonce < 256 so bytes([nonce]) works too.
    prf_input = seed + bytes([nonce]) 
    
    # 2. Get 128 bytes from SHAKE-256 (enough for 256 coeffs when ETA=2)
    # 1 byte = 8 bits = 2 coeffs (4 bits each)
    noise_bytes = shake_256(prf_input).digest(128)
    
    # 3. Process each byte
    for byte in noise_bytes:
        # --- Coefficient 1 (Lower 4 bits) ---
        t = byte & 0x0F        # Take lower 4 bits
        # Sum first 2 bits (a) minus Sum next 2 bits (b)
        # a = bit0 + bit1
        # b = bit2 + bit3
        d1 = ((t >> 0) & 1) + ((t >> 1) & 1) - ((t >> 2) & 1) - ((t >> 3) & 1)
        
        # --- Coefficient 2 (Upper 4 bits) ---
        t = (byte >> 4) & 0x0F # Take upper 4 bits
        d2 = ((t >> 0) & 1) + ((t >> 1) & 1) - ((t >> 2) & 1) - ((t >> 3) & 1)
        
        coeffs.append(d1)
        coeffs.append(d2)
        
    return coeffs

def g_hash_function(data: None|bytes=None) -> tuple[bytes, bytes]:
    """
    Expands a 32-byte seed into two 32-byte seeds (rho, sigma).
    Uses SHA3-512.
    """
    if not data:
        data = secrets.token_bytes(32)
    digest = sha3_512(data).digest()
    return digest[:32], digest[32:]

def h_hash_function(data: bytes):
    return sha3_256(data).digest()

def j_hash_function(data: bytes):
    return shake_256(data).digest(32)