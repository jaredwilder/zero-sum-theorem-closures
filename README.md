# Finite zero-sum derivation system

A finite mathematical derivation system seeded by 27 statements and closed under an explicit set of rules. Exhaustive iteration reaches a fixed point after seven generations with **889 distinct typed statements**.

## Closure size

[`rsi-local-closure/final-receipt.json`](rsi-local-closure/final-receipt.json) records:

| quantity | value |
|---|---:|
| seed statements | 27 |
| generations to fixed point | 7 |
| final statements | **889** |
| newly derived | 862 |

The theorem families include affine-orbit identities, coefficient orbits, all-length digit statements, density comparisons, and other finite consequences of the declared seed/rule system.

“Fixed point” has its literal finite meaning here: running the same derivation rules once more produces no new statement.

## Independent replay

[`rsi-local-closure/independent-verification.json`](rsi-local-closure/independent-verification.json) records a deterministic reconstruction of the closure.

The replay checks:

- **10,528,320 direct assignments**;
- 50 carry statements;
- the theorem-bank digest;
- every individual artifact hash;
- generation-by-generation closure counts.

The 889-object bank can therefore be regenerated from the explicit seeds and rules rather than trusted as a static archive.

## Large derived certificate

`rsi-zero-dollar-proof/` contains a multigeneration certificate built around the order-7 Pascal-derived coefficient vector

\[
[231,-77,-385,385,77,11,-11,-231]
\]

on a domain extending to

\[
76{,}686{,}282{,}021{,}340{,}161.
\]

The package records the scale, coordinate permutation, parent statements, and SHA-256 lineage of each derived object. It also includes a Lean receipt for a Sidon digit obstruction.

## Additional finite mathematics

The repository also contains separate research packages:

- `theorem-forge/three-way-2026-08-04/` — 32 derived statements from a 174-claim Erdős #595/#738 source bank, with back-transfers producing 206 indexed statements;
- `erdos1038/` — 47 finite optimization and self-similarity receipts tied to explicit parameter ranges.

The focused mathematical homes for the #595 and #738 programs are [`triangle-cover-number`](https://github.com/jaredwilder/triangle-cover-number), [`erdos595-barrier-tower`](https://github.com/jaredwilder/erdos595-barrier-tower), and [`erdos738-triangle-free-induced-trees`](https://github.com/jaredwilder/erdos738-triangle-free-induced-trees).

## Scope

The headline result is exhaustive closure of one finite typed derivation system under its stated rules. It does not mean that every statement is historically novel or that a larger open problem is solved by the count itself.

Author: Jared Wilder. License: Apache-2.0.
