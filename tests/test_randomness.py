import pytest
from pyber.params import Q, N
from pyber.randomness import generate_uniform, generate_noise

def test_generate_uniform_determinism():
    """Test that the same seed produces the same polynomial coefficients."""
    seed = b'test_seed_1234567890123456789012' # 32 bytes usually, but any bytes work for SHAKE
    
    coeffs1 = generate_uniform(seed)
    coeffs2 = generate_uniform(seed)
    
    assert coeffs1 == coeffs2
    assert len(coeffs1) == N
    
def test_generate_uniform_range():
    """Test that all generated coefficients are in [0, Q-1]."""
    seed = b'another_seed'
    coeffs = generate_uniform(seed)
    
    for c in coeffs:
        assert 0 <= c < Q

def test_generate_uniform_distinct_seeds():
    """Test that different seeds produce different outputs (high probability)."""
    seed1 = b'seed_A'
    seed2 = b'seed_B'
    
    coeffs1 = generate_uniform(seed1)
    coeffs2 = generate_uniform(seed2)
    
    assert coeffs1 != coeffs2

def test_generate_noise_same_nonce():
    seed = b'test_seed_1234567890123456789012' # 32 bytes usually, but any bytes work for SHAKE
    noise1 = generate_noise(seed, 1)
    noise2 = generate_noise(seed, 1)
    
    assert noise1 == noise2
    assert all(abs(num) <= 2 for num in noise1)

def test_generate_noise_diffrent_nonce():
    seed = b'test_seed_1234567890123456789012' # 32 bytes usually, but any bytes work for SHAKE
    noise1 = generate_noise(seed, 1)
    noise2 = generate_noise(seed, 2)

    assert noise1 != noise2

