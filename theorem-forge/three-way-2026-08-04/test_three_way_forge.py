from __future__ import annotations

import json
import sys
import unittest
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from three_way_forge import Claim, Forge, Rule, SAFE_EXACT, build_rules, generated_claim, parse_595, parse_738, parse_cross

S738 = ROOT / "ERDOS-738-ENCIRCLEMENT-THEOREM-BANK-2026-08-04(1).md"
S595 = ROOT / "ERDOS-595-ENCIRCLEMENT-THEOREM-REFINERY-2026-08-04.md"
SX = ROOT / "ERDOS-738-X-595-CROSS-THEOREM-CARDS-2026-08-04.jsonl"


class ThreeWayForgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = parse_738(S738) + parse_595(S595) + parse_cross(SX)
        cls.forge = Forge(cls.sources, build_rules(), recursive=True)
        cls.forge.run()

    def test_source_counts(self):
        self.assertEqual(len(parse_738(S738)), 62)
        self.assertEqual(len(parse_595(S595)), 65)
        self.assertEqual(len(parse_cross(SX)), 47)

    def test_recursive_count(self):
        self.assertEqual(len(self.forge.generated), 32)

    def test_semantic_hashes_unique(self):
        hashes = [c.claim_hash for c in self.forge.generated]
        self.assertEqual(len(hashes), len(set(hashes)))

    def test_exact_authority_requires_exact_dependencies(self):
        for c in self.forge.generated:
            if c.status in SAFE_EXACT:
                self.assertTrue(all(self.forge.claims[d].status in SAFE_EXACT for d in c.dependencies), c.uid)

    def test_novelty_unrun(self):
        self.assertTrue(all(c.novelty_status == "UNRUN" for c in self.forge.generated))

    def test_back_transfer_all_hybrid(self):
        self.assertTrue(all("HYBRID" in c.back_transfer for c in self.forge.generated))

    def test_control_is_weaker(self):
        control = Forge(self.sources, build_rules(), recursive=False)
        control.run()
        self.assertGreater(len(self.forge.generated), len(control.generated))

    def test_close_programs_remain_open(self):
        self.assertTrue(all(p.unresolved for p in self.forge.close_programs.values()))

    def test_retraction_propagates(self):
        f = Forge(self.sources, build_rules(), recursive=True)
        f.run()
        invalid = set(f.retract("R:R2-STABLECERT"))
        self.assertIn("R:R3-COMMONBOOK", invalid)
        self.assertIn("R:R4-PAGECERT", invalid)

    def test_duplicate_semantic_statement_refused(self):
        dep = self.sources[0].uid
        a = generated_claim(uid="T:D1", title="d1", statement="duplicate exact statement", status="PROVED_IN_PACKET", proof="p", falsifier="f", deps=(dep,), tags=("t",), back=("HYBRID",), lean="d1", novelty="d", leverage=1, round_no=1, rule_id="D1")
        b = generated_claim(uid="T:D2", title="d2", statement="duplicate exact statement", status="PROVED_IN_PACKET", proof="p", falsifier="f", deps=(dep,), tags=("t",), back=("HYBRID",), lean="d2", novelty="d", leverage=1, round_no=1, rule_id="D2")
        f = Forge(self.sources, [Rule("D1", 1, (dep,), a), Rule("D2", 1, (dep,), b)], recursive=True)
        f.run(max_round=1)
        self.assertEqual(len(f.generated), 1)
        self.assertTrue(f.round_receipts[0].duplicate_rejections)

    def test_unknown_dependency_refused(self):
        c = generated_claim(uid="T:U", title="u", statement="unknown premise statement", status="PROVED_IN_PACKET", proof="p", falsifier="f", deps=("UNKNOWN",), tags=("t",), back=("HYBRID",), lean="u", novelty="u", leverage=1, round_no=1, rule_id="U")
        f = Forge(self.sources, [Rule("U", 1, ("UNKNOWN",), c)], recursive=True)
        f.run(max_round=1)
        self.assertFalse(f.generated)

    def test_artifacts_exist(self):
        for name in [
            "FINAL-VERIFICATION.json", "FINITE-MATH-VERIFICATION.json", "HOSTILE-VERIFICATION.json",
            "CAUSAL-ABLATION.json", "RECURSIVE-THEOREM-BANK.md", "LEAN-MISSIONS.jsonl",
            "NOVELTY-MISSIONS.jsonl", "BACK-TRANSFER-QUEUE.json", "ATTACK-QUEUE.json",
        ]:
            self.assertTrue((HERE / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
