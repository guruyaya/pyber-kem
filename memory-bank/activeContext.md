# Active Context

  This file tracks the project's current status, including recent changes, current goals, and open questions.
  2026-02-07 21:20:00 - Randomness implementation completed.

*

## Current Focus

* Implementing Key Generation (KeyGen) logic using the new `Polynomial` factory methods.
* Verify KeyGen against known test vectors (future step).

## Recent Changes

* **2026-02-07 - Randomness Implementation:**
    *   Created `pyber/randomness.py` with `generate_uniform` (SHAKE-128 + Rejection Sampling) and `generate_noise` (SHAKE-256 + CBD).
    *   Updated `Polynomial` class with factory methods `random_uniform(seed)` and `random_noise(seed, nonce)`.
    *   Added comprehensive tests in `tests/test_randomness.py`.
* **2026-02-05 - Matrix Operations:** Implemented `mat_vec_mul` (Matrix-Vector Multiplication) in `pyber/matrix.py`. Verified with tests including Identity and Swap matrices.
* **2026-02-05 - Polynomial Enhancements:**
    *   Added Scalar Multiplication (`__mul__` with int).
    *   Added `zero()` and `one()` class methods.
    *   Refactored naive multiplication logic.

## Open Questions/Issues

* **Performance:** Naive multiplication is slow ($O(n^2)$). NTT implementation is deferred but necessary for production speed.
* **CBD Generalization:** Currently `generate_noise` is hardcoded for `ETA=2` (Kyber-768/1024). Need to support `ETA=3` if Kyber-512 is required.
