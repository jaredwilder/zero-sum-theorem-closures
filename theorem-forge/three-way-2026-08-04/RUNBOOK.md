# Three-Way Recursive Theorem Forge — Runbook

## Inputs

Place these source artifacts in `/mnt/data` or change the paths below:

- `ERDOS-738-ENCIRCLEMENT-THEOREM-BANK-2026-08-04(1).md`
- `ERDOS-595-ENCIRCLEMENT-THEOREM-REFINERY-2026-08-04.md`
- `ERDOS-738-X-595-CROSS-THEOREM-CARDS-2026-08-04.jsonl`

## Build and run

```bash
python three_way_forge.py \
  --source-738 ../ERDOS-738-ENCIRCLEMENT-THEOREM-BANK-2026-08-04\(1\).md \
  --source-595 ../ERDOS-595-ENCIRCLEMENT-THEOREM-REFINERY-2026-08-04.md \
  --source-cross ../ERDOS-738-X-595-CROSS-THEOREM-CARDS-2026-08-04.jsonl \
  --out .

python materialize_outputs.py
```

## Prove the system

```bash
python verify_three_way_forge.py
python -m unittest -v test_three_way_forge.py
```

The verifier must emit `"passed": true` and preserve:

- `FINAL-VERIFICATION.json`
- `FINITE-MATH-VERIFICATION.json`
- `HOSTILE-VERIFICATION.json`
- `CAUSAL-ABLATION.json`
- `REPLAY-VERIFICATION.json`
- `CLEAN-PROCESS-REPLAY.json`

## Local novelty run

Ingest `NOVELTY-MISSIONS.jsonl`. Bind every result to `claim_hash`. “No collision found” is not global novelty.

## Local Lean run

Ingest `LEAN-MISSIONS.jsonl`. Promote only after kernel acceptance, semantic binding, and axiom audit.

## First attack order

1. `R:R2-STABLECERT` — Stable Certification of Omitted Edges.
2. `R:R3-COMMONBOOK` — Common Omitted-Edge Stable Book.
3. `R:R4-PAGECERT` — Minimal-Transversal Page Certificates.
4. `R:R3-TWOLAYER` — Two-Layer Cross-Fiber Purification.
5. `R:R4-CENSUS` — Canonical Combined-State Census.
6. `R:R4-MULTIBOOK` — Multi-Book Interaction Frontier.

## Claim boundary

The build verifies the recursive engine and selected finite kernels. It does not claim Erdős #738 or #595 is closed, does not infer novelty, and did not run Lean in this environment.
