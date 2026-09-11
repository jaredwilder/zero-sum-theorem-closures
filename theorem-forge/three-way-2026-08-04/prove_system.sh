#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
python "$HERE/three_way_forge.py" \
  --source-738 "$ROOT/ERDOS-738-ENCIRCLEMENT-THEOREM-BANK-2026-08-04(1).md" \
  --source-595 "$ROOT/ERDOS-595-ENCIRCLEMENT-THEOREM-REFINERY-2026-08-04.md" \
  --source-cross "$ROOT/ERDOS-738-X-595-CROSS-THEOREM-CARDS-2026-08-04.jsonl" \
  --out "$HERE"
python "$HERE/materialize_outputs.py"
python "$HERE/verify_three_way_forge.py"
python -m unittest -v "$HERE/test_three_way_forge.py"
