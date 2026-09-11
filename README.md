# Finite theorem closure and zero-sum derivations

A finite derivation system starting from **27 seed statements** reaches a fixed point after **7 generations**, producing **889 typed theorems**. The complete closure was independently re-executed and checked by direct computation.

Author: Jared Wilder. First public timestamp: 2026-09-10. Work dated 2026-08-04.

## The 889-theorem closure

`rsi-local-closure/final-receipt.json` records the fixed point:

| | |
|---|---:|
| seeds | 27 |
| generations | 7 |
| final theorem count | **889** |
| newly derived | 862 |
| growth by generation | 128, 176, 176, ... then no new statements |

By type, the closure includes 151 affine-orbit theorems, 50 all-length-digit theorems, 25 coefficient-orbit theorems, 7 best-density statements, and further families. “Saturated” here has a precise finite meaning: applying the declared derivation rules again at generation 8 produced nothing new.

## Independent replay

`rsi-local-closure/independent-verification.json` records a deterministic re-execution of the closure:

- **10,528,320 direct assignments checked**;
- 50 carry theorems checked;
- receipt hash, theorem-bank hash, and every individual artifact hash re-verified;
- the verification used no language-model calls.

The important point is reproducibility: the theorem bank can be regenerated and checked from its explicit rules and inputs rather than accepted on review alone.

## A large derived certificate

`rsi-zero-dollar-proof/` contains a multigeneration reuse certificate, including an order-7 Pascal-derived coefficient vector

`[231, −77, −385, 385, 77, 11, −11, −231]`

over a domain extending to `76,686,282,021,340,161`, together with a Lean receipt for a **Sidon digit obstruction**.

Each derived object records its scale, permutation, and SHA-256 parentage so the derivation history can be replayed.

## Erdős 595 and 738 theorem bank

`theorem-forge/three-way-2026-08-04/` contains 32 derived theorems from 174 source claims, unified to 206 statements after back-transfers, plus seven high-leverage rules prepared for Lean formalization.

Statements proved in the packet and still-open checkable targets are kept in separate classes.

## Erdős 1038 finite optimization work

`erdos1038/` contains 47 receipts from LP minimization, growth and cusp analysis, variation profiles, and self-similarity computations. Each result is tied to its stated parameter range.

## Scope

The **889-theorem headline concerns the complete closure of one finite typed derivation system under its declared rules**. The statements are consequences of the supplied seeds; the mathematical contribution is the exhaustive closure and its reproducible derivation structure.

The Erdős 595, 738, and 1038 material is separate and carries its own statement-by-statement evidence.

## License

Apache-2.0.