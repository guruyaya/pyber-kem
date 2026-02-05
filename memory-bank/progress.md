# Progress

This file tracks the project's progress using a task list format.
2026-02-05 08:51:00 - Log of updates made.

*

## Completed Tasks

* [x] 2026-02-04 10:45:55 - Explained high-level concept of ML-KEM (Kyber) and Lattice-based cryptography.
* [x] 2026-02-04 10:46:21 - Defined the first component to implement: Polynomial representation and arithmetic over a finite field.
* [x] 2026-02-04 11:28:00 - Guided user through TDD setup: Created project, wrote first test, implemented `Polynomial` class with modular reduction.
* [x] 2026-02-04 13:30:00 - Implemented Polynomial Addition and Subtraction.
* [x] 2026-02-04 13:30:00 - Implemented Polynomial Multiplication (Naive $O(n^2)$) verified with robust corner-case tests.
* [x] 2026-02-05 01:27:00 - Implemented Matrix-Vector Multiplication (`mat_vec_mul`) correctly handling row-vector products.

## Current Tasks

* Implement Random Polynomial Generation:
    * `random_uniform()`: For matrix $A$.
    * `random_small()`: For secrets $\mathbf{s}, \mathbf{e}$ (using simple random for now, later CBD).
* Implement Key Generation: Combine Matrix * Vector + Noise.

## Next Steps

* Implement Compression/Decompression functions.
* Implement Encapsulation.
* Implement Decapsulation.
* (Deferred) Implement Number Theoretic Transform (NTT) for optimization.