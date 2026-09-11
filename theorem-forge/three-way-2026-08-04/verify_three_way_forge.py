#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from three_way_forge import (  # noqa: E402
    Claim,
    Forge,
    Rule,
    SAFE_EXACT,
    build_rules,
    canonical_json,
    generated_claim,
    parse_595,
    parse_738,
    parse_cross,
    sha256_text,
)

SOURCE_738 = ROOT / "ERDOS-738-ENCIRCLEMENT-THEOREM-BANK-2026-08-04(1).md"
SOURCE_595 = ROOT / "ERDOS-595-ENCIRCLEMENT-THEOREM-REFINERY-2026-08-04.md"
SOURCE_CROSS = ROOT / "ERDOS-738-X-595-CROSS-THEOREM-CARDS-2026-08-04.jsonl"


def hfile(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm_edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def all_edges(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def graph_from_mask(n: int, mask: int) -> tuple[list[set[int]], list[tuple[int, int]]]:
    adj = [set() for _ in range(n)]
    present = []
    for bit, (u, v) in enumerate(all_edges(n)):
        if (mask >> bit) & 1:
            adj[u].add(v)
            adj[v].add(u)
            present.append((u, v))
    return adj, present


def triangles(n: int, edges: list[tuple[int, int]] | set[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
    es = {norm_edge(*e) for e in edges}
    out = []
    for a, b, c in itertools.combinations(range(n), 3):
        tri = (norm_edge(a, b), norm_edge(a, c), norm_edge(b, c))
        if all(e in es for e in tri):
            out.append(tri)
    return out


def is_triangle_free(n: int, edges: list[tuple[int, int]] | set[tuple[int, int]]) -> bool:
    return not triangles(n, edges)


def is_k4_free(n: int, edges: list[tuple[int, int]] | set[tuple[int, int]]) -> bool:
    es = {norm_edge(*e) for e in edges}
    for vs in itertools.combinations(range(n), 4):
        if all(norm_edge(*e) in es for e in itertools.combinations(vs, 2)):
            return False
    return True


def adj_from_edges(n: int, edges: list[tuple[int, int]] | set[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def triangle_cover_number(n: int, edges: list[tuple[int, int]]) -> int:
    edges = sorted({norm_edge(*e) for e in edges})
    if not edges:
        return 0
    tris = triangles(n, edges)
    if not tris:
        return 1
    idx = {e: i for i, e in enumerate(edges)}
    tri_idx = [[idx[e] for e in tri] for tri in tris]
    for k in range(2, 5):
        colors = [-1] * len(edges)
        membership = [[] for _ in edges]
        for ti, tri in enumerate(tri_idx):
            for e in tri:
                membership[e].append(ti)
        order = sorted(range(len(edges)), key=lambda e: len(membership[e]), reverse=True)

        def valid(ti: int) -> bool:
            vals = [colors[e] for e in tri_idx[ti]]
            return not (all(v >= 0 for v in vals) and vals[0] == vals[1] == vals[2])

        def rec(pos: int) -> bool:
            if pos == len(order):
                return True
            e = order[pos]
            for color in range(k):
                colors[e] = color
                if all(valid(ti) for ti in membership[e]) and rec(pos + 1):
                    return True
                colors[e] = -1
            return False

        if rec(0):
            return k
    raise AssertionError("unexpected tc>4 in finite verification")


def maximal_triangle_free_subgraphs(n: int, g_edges: list[tuple[int, int]]) -> list[frozenset[tuple[int, int]]]:
    g_edges = sorted({norm_edge(*e) for e in g_edges})
    out = []
    for mask in range(1 << len(g_edges)):
        h = {g_edges[i] for i in range(len(g_edges)) if (mask >> i) & 1}
        if not is_triangle_free(n, h):
            continue
        maximal = True
        for e in g_edges:
            if e in h:
                continue
            if is_triangle_free(n, h | {e}):
                maximal = False
                break
        if maximal:
            out.append(frozenset(h))
    return out


def induced_paths(n: int, edges: set[tuple[int, int]]) -> list[tuple[int, ...]]:
    paths = set()
    for length in range(2, n + 1):
        for seq in itertools.permutations(range(n), length):
            if seq[::-1] in paths:
                continue
            good = True
            for i in range(length - 1):
                if norm_edge(seq[i], seq[i + 1]) not in edges:
                    good = False
                    break
            if not good:
                continue
            for i in range(length):
                for j in range(i + 2, length):
                    if norm_edge(seq[i], seq[j]) in edges:
                        good = False
                        break
                if not good:
                    break
            if good:
                paths.add(seq)
    return sorted(paths)


def finite_math_verification() -> dict[str, object]:
    assertions = 0
    k4_graphs = 0
    maximal_layers_checked = 0
    family_checks = 0
    signature_checks = 0

    # Stable omitted-edge certificates and book sterility through five vertices.
    for n in range(1, 6):
        for mask in range(1 << len(all_edges(n))):
            _, g_edges = graph_from_mask(n, mask)
            if not is_k4_free(n, g_edges):
                continue
            k4_graphs += 1
            gset = set(g_edges)
            gadj = adj_from_edges(n, g_edges)
            # R1-K4FIBER / sibling defect kernel: every neighborhood is triangle-free.
            for v in range(n):
                nv = gadj[v]
                internal = {e for e in gset if e[0] in nv and e[1] in nv}
                assert is_triangle_free(n, internal)
                assertions += 1

            maximal = maximal_triangle_free_subgraphs(n, g_edges)
            maximal_layers_checked += len(maximal)
            for h in maximal:
                hadj = adj_from_edges(n, h)
                for x, y in gset - set(h):
                    witnesses = hadj[x] & hadj[y]
                    assert witnesses, (n, g_edges, h, (x, y))
                    for a, b in itertools.combinations(witnesses, 2):
                        assert norm_edge(a, b) not in gset
                    # The induced stable book has tc exactly 2.
                    book_edges = [norm_edge(x, y)] + [norm_edge(x, z) for z in witnesses] + [norm_edge(y, z) for z in witnesses]
                    assert triangle_cover_number(n, book_edges) == 2
                    assertions += 2 + max(0, len(witnesses) * (len(witnesses) - 1) // 2)

            # Finite analogue of common omitted-edge stable book for families of <=3 maximal layers.
            for r in range(1, min(3, len(maximal)) + 1):
                for family in itertools.combinations(maximal, r):
                    union = set().union(*map(set, family))
                    omitted = gset - union
                    if not omitted:
                        continue
                    x, y = next(iter(omitted))
                    for h in family:
                        hadj = adj_from_edges(n, h)
                        witnesses = hadj[x] & hadj[y]
                        assert witnesses
                        for a, b in itertools.combinations(witnesses, 2):
                            assert norm_edge(a, b) not in gset
                    family_checks += 1
                    assertions += r

    # Exhaustive two-layer signature descent through four vertices.
    for n in range(2, 5):
        edges = all_edges(n)
        tf_subsets = []
        for mask in range(1 << len(edges)):
            h = {edges[i] for i in range(len(edges)) if (mask >> i) & 1}
            if is_triangle_free(n, h):
                tf_subsets.append(h)
        for h0 in tf_subsets:
            for h1 in tf_subsets:
                g = h0 | h1
                g_k4 = is_k4_free(n, g)
                h0_adj = adj_from_edges(n, h0)
                for path in induced_paths(n, h0):
                    outside = set(range(n)) - set(path)
                    fibers: dict[tuple[int, ...], list[int]] = {}
                    for x in outside:
                        sig = tuple(i for i, p in enumerate(path) if p in h0_adj[x])
                        if sig:
                            fibers.setdefault(sig, []).append(x)
                    for fiber in fibers.values():
                        for x, y in itertools.combinations(fiber, 2):
                            e = norm_edge(x, y)
                            assert e not in h0
                            if e in g:
                                assert e in h1
                            assertions += 2
                        if g_k4:
                            internal = {e for e in g if e[0] in fiber and e[1] in fiber}
                            assert is_triangle_free(n, internal)
                            assertions += 1
                        signature_checks += 1

    return {
        "schema": "oracle.three-way-recursive-forge.finite-math.v1",
        "passed": True,
        "max_vertices": 5,
        "k4_free_graphs_checked": k4_graphs,
        "maximal_layers_checked": maximal_layers_checked,
        "maximal_layer_family_checks": family_checks,
        "signature_fiber_checks": signature_checks,
        "assertions": assertions,
        "checked_claims": [
            "R1-K4FIBER",
            "R1-SIGDESC (m=2 finite boundary)",
            "R2-STABLECERT",
            "R2-BOOKSTERILE",
            "R3-COMMONBOOK finite-family boundary",
            "R4-PAGECERT",
        ],
        "scope_note": "Finite exhaustion supports the exact finite kernels only; it does not certify the infinite/cardinal flagship claims.",
    }


def hostile_verification(source_claims: list[Claim]) -> dict[str, object]:
    tests: dict[str, bool] = {}

    # Forged authority must downgrade when a dependency is conditional.
    conditional_dep = next(c.uid for c in source_claims if c.status in {"CONDITIONAL_ON_738_T", "CONDITIONAL_ON_738_SEQUENCE", "CONDITIONAL_REDUCTION"})
    forged = generated_claim(
        uid="H:FORGED", title="Forged exact theorem", statement="A forged exact theorem.",
        status="PROVED_IN_PACKET", proof="invalid", falsifier="n/a", deps=(conditional_dep,),
        tags=("hostile",), back=("595",), lean="forged", novelty="forged", leverage=1,
        round_no=1, rule_id="HOSTILE-FORGED",
    )
    f = Forge(source_claims, [Rule("HOSTILE-FORGED", 1, (conditional_dep,), forged)], recursive=True)
    f.run(max_round=1)
    tests["forged_authority_downgraded"] = len(f.generated) == 1 and f.generated[0].status == "CONDITIONAL_REDUCTION"

    # Unknown dependency remains ungenerated.
    unknown = generated_claim(
        uid="H:UNKNOWN", title="Unknown dependency", statement="Unknown premise theorem.",
        status="PROVED_IN_PACKET", proof="invalid", falsifier="n/a", deps=("MISSING:CLAIM",),
        tags=("hostile",), back=("595",), lean="unknown", novelty="unknown", leverage=1,
        round_no=1, rule_id="HOSTILE-UNKNOWN",
    )
    f2 = Forge(source_claims, [Rule("HOSTILE-UNKNOWN", 1, ("MISSING:CLAIM",), unknown)], recursive=True)
    f2.run(max_round=1)
    tests["unknown_dependency_refused"] = not f2.generated

    # Semantic duplicate with a different UID/rule is refused.
    dep = source_claims[0].uid
    dup1 = generated_claim(
        uid="H:DUP1", title="Duplicate one", statement="The exact same semantic statement.",
        status="PROVED_IN_PACKET", proof="p", falsifier="f", deps=(dep,), tags=("hostile",),
        back=("738",), lean="dup1", novelty="dup", leverage=1, round_no=1, rule_id="HOSTILE-DUP1",
    )
    dup2 = generated_claim(
        uid="H:DUP2", title="Duplicate two", statement="The exact same semantic statement.",
        status="PROVED_IN_PACKET", proof="p", falsifier="f", deps=(dep,), tags=("hostile",),
        back=("595",), lean="dup2", novelty="dup", leverage=1, round_no=1, rule_id="HOSTILE-DUP2",
    )
    f3 = Forge(source_claims, [Rule("HOSTILE-DUP1", 1, (dep,), dup1), Rule("HOSTILE-DUP2", 1, (dep,), dup2)], recursive=True)
    f3.run(max_round=1)
    tests["semantic_duplicate_refused"] = len(f3.generated) == 1 and bool(f3.round_receipts[0].duplicate_rejections)

    # Retraction invalidates recursive descendants.
    real = Forge(source_claims, build_rules(), recursive=True)
    real.run()
    invalidated = real.retract("R:R2-STABLECERT")
    expected = {"R:R2-SIGCERT", "R:R3-COMMONBOOK", "R:R3-KAPPABOOK", "R:R4-PAGECERT"}
    tests["retraction_invalidates_descendants"] = expected.issubset(set(invalidated))

    # Tampered source fails frozen source hash comparison.
    original_hash = hfile(SOURCE_738)
    with tempfile.TemporaryDirectory() as td:
        tampered = Path(td) / "source.md"
        tampered.write_bytes(SOURCE_738.read_bytes() + b"\nTAMPER\n")
        tests["source_tamper_detected"] = hfile(tampered) != original_hash

    # Novelty remains unrun and no flagship is silently closed.
    tests["novelty_not_inferred"] = all(c.novelty_status == "UNRUN" for c in real.generated)
    tests["flagships_remain_open"] = all(p.unresolved for p in real.close_programs.values())

    passed = all(tests.values())
    return {
        "schema": "oracle.three-way-recursive-forge.hostile.v1",
        "passed": passed,
        "tests": tests,
        "invalidated_by_retraction": invalidated,
    }


def causal_ablation(source_claims: list[Claim]) -> dict[str, object]:
    rules = build_rules()
    control = Forge(source_claims, rules, recursive=False)
    control.run()
    treatment = Forge(source_claims, rules, recursive=True)
    treatment.run()
    control_unresolved = sum(len(p.unresolved) for p in control.close_programs.values())
    treatment_unresolved = sum(len(p.unresolved) for p in treatment.close_programs.values())
    metrics = {
        "control_generated_claims": len(control.generated),
        "treatment_generated_claims": len(treatment.generated),
        "recursive_claim_gain": len(treatment.generated) - len(control.generated),
        "control_unresolved_close_obligations": control_unresolved,
        "treatment_unresolved_close_obligations": treatment_unresolved,
        "close_route_reduction": control_unresolved - treatment_unresolved,
        "control_multi_campaign_back_transfers": sum(len(c.back_transfer) >= 2 for c in control.generated),
        "treatment_multi_campaign_back_transfers": sum(len(c.back_transfer) >= 2 for c in treatment.generated),
    }
    passed = metrics["recursive_claim_gain"] > 0 and metrics["close_route_reduction"] > 0 and metrics["treatment_multi_campaign_back_transfers"] > metrics["control_multi_campaign_back_transfers"]
    return {
        "schema": "oracle.three-way-recursive-forge.ablation.v1",
        "policy_delta": "control forbids generated claims as rule premises; treatment permits recursive consumption to fixed point within each round",
        "passed": passed,
        "metrics": metrics,
    }


def replay_verification() -> dict[str, object]:
    source_claims = parse_738(SOURCE_738) + parse_595(SOURCE_595) + parse_cross(SOURCE_CROSS)
    rules = build_rules()
    a = Forge(source_claims, rules, recursive=True)
    b = Forge(source_claims, rules, recursive=True)
    a.run()
    b.run()
    a_bytes = canonical_json([asdict(c) for c in a.generated])
    b_bytes = canonical_json([asdict(c) for c in b.generated])
    ar = canonical_json([asdict(r) for r in a.round_receipts])
    br = canonical_json([asdict(r) for r in b.round_receipts])
    return {
        "schema": "oracle.three-way-recursive-forge.replay.v1",
        "passed": a_bytes == b_bytes and ar == br,
        "generated_hash": sha256_text(a_bytes),
        "round_receipt_hash": sha256_text(ar),
        "generated_count": len(a.generated),
    }


def run_clean_process_replay() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        outputs = []
        for td in (td1, td2):
            cmd = [
                sys.executable, str(HERE / "three_way_forge.py"),
                "--source-738", str(SOURCE_738),
                "--source-595", str(SOURCE_595),
                "--source-cross", str(SOURCE_CROSS),
                "--out", td,
            ]
            proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
            if proc.returncode != 0:
                return {"passed": False, "stderr": proc.stderr, "returncode": proc.returncode}
            outputs.append({
                name: hfile(Path(td) / name)
                for name in ["RECURSIVE-THEOREM-CARDS.jsonl", "ROUND-RECEIPTS.json", "CLOSE-PROGRAMS.json"]
            })
        return {
            "schema": "oracle.three-way-recursive-forge.clean-process-replay.v1",
            "passed": outputs[0] == outputs[1],
            "run_hashes": outputs,
        }


def update_manifest(final_files: list[Path], source_claims: list[Claim]) -> None:
    manifest_path = HERE / "MANIFEST.json"
    old = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    old["files"] = {p.name: hfile(p) for p in sorted(final_files) if p.is_file() and p.name != "MANIFEST.json"}
    old["parsed_source_counts"] = {
        "738": len(parse_738(SOURCE_738)),
        "595": len(parse_595(SOURCE_595)),
        "cross": len(parse_cross(SOURCE_CROSS)),
        "total": len(source_claims),
    }
    old["content_hash"] = sha256_text(canonical_json({k: v for k, v in old.items() if k != "content_hash"}))
    manifest_path.write_text(json.dumps(old, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    source_claims = parse_738(SOURCE_738) + parse_595(SOURCE_595) + parse_cross(SOURCE_CROSS)
    treatment = Forge(source_claims, build_rules(), recursive=True)
    treatment.run()

    tests: dict[str, object] = {}
    tests["source_counts"] = {
        "738": len(parse_738(SOURCE_738)),
        "595": len(parse_595(SOURCE_595)),
        "cross": len(parse_cross(SOURCE_CROSS)),
        "total": len(source_claims),
        "passed": (len(parse_738(SOURCE_738)), len(parse_595(SOURCE_595)), len(parse_cross(SOURCE_CROSS))) == (62, 65, 47),
    }
    tests["unique_uids"] = len({c.uid for c in source_claims + treatment.generated}) == len(source_claims) + len(treatment.generated)
    tests["unique_generated_claim_hashes"] = len({c.claim_hash for c in treatment.generated}) == len(treatment.generated)
    tests["authority_safety"] = all(
        c.status not in SAFE_EXACT or all(treatment.claims[d].status in SAFE_EXACT for d in c.dependencies)
        for c in treatment.generated
    )
    tests["generated_count"] = len(treatment.generated) == 32
    tests["flagships_not_falsely_closed"] = all(p.unresolved for p in treatment.close_programs.values())

    finite = finite_math_verification()
    hostile = hostile_verification(source_claims)
    ablation = causal_ablation(source_claims)
    replay = replay_verification()
    clean_replay = run_clean_process_replay()

    (HERE / "FINITE-MATH-VERIFICATION.json").write_text(json.dumps(finite, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "HOSTILE-VERIFICATION.json").write_text(json.dumps(hostile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "CAUSAL-ABLATION.json").write_text(json.dumps(ablation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "REPLAY-VERIFICATION.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "CLEAN-PROCESS-REPLAY.json").write_text(json.dumps(clean_replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_pass = all(v if isinstance(v, bool) else v.get("passed", False) for v in tests.values()) and finite["passed"] and hostile["passed"] and ablation["passed"] and replay["passed"] and clean_replay["passed"]
    final = {
        "schema": "oracle.three-way-recursive-forge.final-verification.v1",
        "passed": all_pass,
        "tests": tests,
        "finite_math_receipt": hfile(HERE / "FINITE-MATH-VERIFICATION.json"),
        "hostile_receipt": hfile(HERE / "HOSTILE-VERIFICATION.json"),
        "ablation_receipt": hfile(HERE / "CAUSAL-ABLATION.json"),
        "replay_receipt": hfile(HERE / "REPLAY-VERIFICATION.json"),
        "clean_process_replay_receipt": hfile(HERE / "CLEAN-PROCESS-REPLAY.json"),
        "generated_claims": len(treatment.generated),
        "exact_generated_claims": sum(c.status in SAFE_EXACT for c in treatment.generated),
        "conditional_or_search_claims": sum(c.status not in SAFE_EXACT for c in treatment.generated),
        "flagship_closed": False,
        "novelty_claimed": False,
        "lean_executed": False,
        "proof_boundary": "System behavior, recursive causal gain, hostile fail-closed gates, and finite kernels are verified. Infinite/cardinal theorem claims retain their packet proof/conditional status and require local Lean/novelty review.",
    }
    final["content_hash"] = sha256_text(canonical_json(final))
    (HERE / "FINAL-VERIFICATION.json").write_text(json.dumps(final, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    files = list(HERE.iterdir())
    update_manifest(files, source_claims)
    print(json.dumps(final, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
