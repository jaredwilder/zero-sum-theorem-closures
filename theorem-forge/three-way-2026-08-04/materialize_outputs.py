#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cards = [json.loads(line) for line in (HERE / 'RECURSIVE-THEOREM-CARDS.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]

# Full markdown theorem bank.
lines = [
    '# Three-Way Recursive Theorem Bank',
    '',
    '**Date:** 2026-08-04  ',
    '**Novelty:** UNRUN  ',
    '**Lean:** UNRUN  ',
    '**Flagship closure:** NONE — exact remaining obligations are retained in `CLOSE-PROGRAMS.json`.',
    '',
    f'**Inventory:** {len(cards)} recursive theorem/target cards.',
    '',
]
for c in cards:
    lines += [
        f"## {c['uid']} — {c['title']}",
        '',
        f"- **Status:** `{c['status']}`",
        f"- **Round:** `{c['round_generated']}`",
        f"- **Rule:** `{c['rule_id']}`",
        f"- **Dependencies:** `{', '.join(c['dependencies'])}`",
        f"- **Tags:** `{', '.join(c['tags'])}`",
        f"- **Back-transfer:** `{', '.join(c['back_transfer'])}`",
        f"- **Structural leverage:** `{c['structural_leverage']}/100`",
        f"- **Claim hash:** `{c['claim_hash']}`",
        '',
        f"**Statement.** {c['statement']}",
        '',
        f"**Proof route.** {c['proof_route']}",
        '',
        f"**Falsifier.** {c['falsifier']}",
        '',
        f"**Lean mission.** `{c['lean_mission']}`",
        '',
        f"**Novelty query.** `{c['novelty_query']}`",
        '',
    ]
(HERE / 'RECURSIVE-THEOREM-BANK.md').write_text('\n'.join(lines).strip() + '\n', encoding='utf-8')

# Lean and novelty mission queues.
with (HERE / 'LEAN-MISSIONS.jsonl').open('w', encoding='utf-8') as f:
    for c in cards:
        f.write(json.dumps({
            'claim_uid': c['uid'],
            'claim_hash': c['claim_hash'],
            'theorem_name': c['lean_mission'],
            'statement': c['statement'],
            'dependencies': c['dependencies'],
            'status_before_lean': c['status'],
            'priority': c['structural_leverage'],
            'acceptance': 'Lean kernel accepts; semantic binding and axiom audit recorded separately.',
        }, ensure_ascii=False, sort_keys=True) + '\n')
with (HERE / 'NOVELTY-MISSIONS.jsonl').open('w', encoding='utf-8') as f:
    for c in cards:
        f.write(json.dumps({
            'claim_uid': c['uid'],
            'claim_hash': c['claim_hash'],
            'exact_statement': c['statement'],
            'query': c['novelty_query'],
            'status': 'UNRUN',
            'global_novelty_claimed': False,
            'nearest_prior_art': None,
        }, ensure_ascii=False, sort_keys=True) + '\n')

# Back-transfer and attack queues.
back = {'738': [], '595': [], 'HYBRID': []}
for c in cards:
    for target in c['back_transfer']:
        back[target].append({
            'claim_uid': c['uid'],
            'title': c['title'],
            'status': c['status'],
            'structural_leverage': c['structural_leverage'],
            'rule_id': c['rule_id'],
        })
for values in back.values():
    values.sort(key=lambda x: (-x['structural_leverage'], x['claim_uid']))
(HERE / 'BACK-TRANSFER-QUEUE.json').write_text(json.dumps(back, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')

attack = [
    {
        'claim_uid': c['uid'], 'title': c['title'], 'status': c['status'],
        'structural_leverage': c['structural_leverage'], 'falsifier': c['falsifier'],
        'back_transfer': c['back_transfer'], 'claim_hash': c['claim_hash'],
    }
    for c in cards if c['status'] in {'UNPROVED_CHECKABLE_TARGET', 'CONDITIONAL_REDUCTION', 'CONDITIONAL_ON_738_SEQUENCE'}
]
attack.sort(key=lambda x: (-x['structural_leverage'], x['claim_uid']))
(HERE / 'ATTACK-QUEUE.json').write_text(json.dumps(attack, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')

print(json.dumps({'cards': len(cards), 'lean_missions': len(cards), 'novelty_missions': len(cards), 'attack_queue': len(attack)}, indent=2))
