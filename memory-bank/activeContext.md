# Active Context

  This file tracks the project's current status, including recent changes, current goals, and open questions.
  2026-02-05 08:50:00 - Log of updates made.

*

## Current Focus

* Implementing Randomness (Uniform and CBD/Small) for Key Generation (KeyGen).
* Deciding on Randomness Source: `secrets` module vs full SHAKE-128 implementation (Standard).

## Recent Changes

* **2026-02-05 - Matrix Operations:** Implemented `mat_vec_mul` (Matrix-Vector Multiplication) in `pyber/matrix.py`. Verified with tests including Identity and Swap matrices.
* **2026-02-05 - Polynomial Enhancements:**
    *   Added Scalar Multiplication (`__mul__` with int).
    *   Added `zero()` and `one()` class methods.
    *   Refactored naive multiplication logic.
* **2026-02-04 - Polynomial Arithmetic:** Implemented Addition, Subtraction, and Multiplication (Naive $O(n^2)$) with modulo reduction.
* **2026-02-04 - Testing:** Established TDD workflow with `pytest`. `test_polynomials.py` and `test_matrix.py` are passing (Green).

## Open Questions/Issues

* **Performance:** Naive multiplication is slow ($O(n^2)$). NTT implementation is deferred but necessary for production speed.
* **Randomness:** Using Python's `secrets` for now, but need to implement SHAKE-128 for spec compliance later.
