# zero-sum-theorem-closures

A deterministic theorem-generation run that saturated to a fixed point: **27 seeds, 7 generations,
889 typed theorems, independently re-verified with zero model calls.** Plus recursive theorem work
on Erdos 595 and 738, and an optimization attack on Erdos 1038.

Author: Jared Wilder. First public timestamp: 2026-09-10. Work dated 2026-08-04.

## The local closure

`rsi-local-closure/final-receipt.json`, verdict `LOCAL_TYPED_CLOSURE_SATURATED`:

| | |
|---|---|
| seeds | 27 |
| generations | 7 |
| final artifact count | **889** |
| newly derived | 862 |
| growth by generation | 128, 176, 176, ... then nothing new |

By type: 151 affine-orbit theorems, 50 all-length-digit theorems, 25 coefficient-orbit, 7
best-density, and the rest across further families. **Saturated** means generation 8 produced
nothing new, so the typed closure of those seeds under those rules is complete and finite.

## The independent verification

`rsi-local-closure/independent-verification.json`, verdict
`LOCAL_TYPED_CLOSURE_INDEPENDENTLY_VERIFIED`:

- **10,528,320 direct assignments checked**
- 50 carry theorems checked
- receipt hash, artifact-bank hash and every individual artifact hash re-verified
- **`modelCalls: 0`** — no language model participated in the verification
- 8.2 seconds

That last line is the point. The verification is a deterministic re-execution, not a review.

## The zero-dollar multigeneration proof

`rsi-zero-dollar-proof/` carries `MULTIGENERATION_ZERO_DOLLAR_RSI_PROVED`, including a mutated
Pascal reuse certificate at order 7 with coefficient vector
[231, −77, −385, 385, 77, 11, −11, −231] over a domain up to 76,686,282,021,340,161, and a Lean
receipt for a **Sidon digit obstruction**.

Each mutation records its scale, its permutation, and the sha256 of the object it was derived from,
so reuse is provable rather than asserted.

## Erdos 595 and 738 recursive theorems

`theorem-forge/three-way-2026-08-04/` — 32 new theorems derived from 174 source claims, unified to
206 with back-transfers, and seven highest-leverage rules with named Lean missions.

Statuses are split honestly between `PROVED_IN_PACKET` and **`UNPROVED_CHECKABLE_TARGET`**. The
second label means exactly what it says: stated precisely enough to be attacked, and not proved.

## Erdos 1038

`erdos1038/` — 47 receipt files from a multi-method optimization attack: LP minimization, growth and
cusp analysis, variation profiles, and self-similarity. **The problem is open and these are
bounds and profiles, not a closure.**

## What is not claimed

None of this closes an Erdos problem. The closure result is a statement about a **typed derivation
system reaching its own fixed point**, not about mathematics running out. The 889 theorems are
elementary consequences of their seeds, and the value is that the derivation is exhaustive,
hash-chained, and replayable without a model in the loop.

## License

Apache-2.0.
