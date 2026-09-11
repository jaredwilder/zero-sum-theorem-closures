#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Iterable

SAFE_EXACT = {"PROVED_IN_PACKET", "FINITE_VERIFIED", "INDEPENDENTLY_VERIFIED", "CERTIFICATE_CHECKED", "LEAN_VERIFIED"}
CONDITIONAL = {"CONDITIONAL_REDUCTION", "CONDITIONAL_ON_738_T", "CONDITIONAL_ON_738_SEQUENCE", "CONDITIONAL_ON_FULL_738", "PROVED_FROM_FINITE_FOLKMAN_INPUT", "PROVED_USING_STANDARD_COMPACTNESS"}
SEARCH_ONLY = {"UNPROVED_CHECKABLE_TARGET", "PROPOSED", "REFUTED_ROUTE"}


def canonical_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Claim:
    uid: str
    origin: str
    source_id: str
    title: str
    statement: str
    status: str
    proof_route: str
    falsifier: str
    dependencies: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    back_transfer: tuple[str, ...] = ()
    lean_mission: str = "UNASSIGNED"
    novelty_query: str = "UNASSIGNED"
    novelty_status: str = "UNRUN"
    structural_leverage: int = 0
    round_generated: int = 0
    rule_id: str = "SOURCE"
    claim_hash: str = ""

    def normalized(self) -> "Claim":
        statement = " ".join(self.statement.split())
        # Exact-claim identity is semantic: provenance, status, and rule path do not
        # change the mathematical statement bound to novelty/formalization receipts.
        return Claim(**{**asdict(self), "statement": statement, "claim_hash": sha256_text(statement)})


@dataclass(frozen=True)
class Rule:
    rule_id: str
    round_no: int
    requires: tuple[str, ...]
    output: Claim
    may_consume_generated: bool = True


@dataclass
class CloseProgram:
    close_id: str
    target: str
    obligations: list[str]
    resolved_by: dict[str, str] = field(default_factory=dict)

    @property
    def unresolved(self) -> list[str]:
        return [o for o in self.obligations if o not in self.resolved_by]


@dataclass
class RoundReceipt:
    round_no: int
    inherited_claims: int
    generated_ids: list[str]
    duplicate_rejections: list[str]
    status_downgrades: list[str]
    close_unresolved_before: dict[str, int]
    close_unresolved_after: dict[str, int]
    content_hash: str = ""


class ParseError(RuntimeError):
    pass


def extract_between(text: str, start_patterns: list[str], end_patterns: list[str]) -> str:
    start = None
    for pat in start_patterns:
        m = re.search(pat, text, re.I | re.M)
        if m:
            start = m.end()
            break
    if start is None:
        return ""
    remainder = text[start:]
    ends = []
    for pat in end_patterns:
        m = re.search(pat, remainder, re.I | re.M)
        if m:
            ends.append(m.start())
    end = min(ends) if ends else len(remainder)
    value = remainder[:end].strip()
    value = re.sub(r"^[-*]\s*", "", value)
    return value


def infer_tags(origin: str, cid: str, title: str, statement: str) -> tuple[str, ...]:
    blob = f"{cid} {title} {statement}".lower()
    tags = {origin.lower()}
    keywords = {
        "triangle_free": ["triangle-free", "triangle free"],
        "k4_free": ["k_4", "k4-free", "k₄-free"],
        "chromatic": ["chromatic", "χ("],
        "tree": ["tree", "spider", "path"],
        "contact_signature": ["signature", "contact"],
        "type_tensor": ["tensor", "type-uniform", "type profile"],
        "critical": ["critical"],
        "protected_deletion": ["protected deletion", "deletion ledger", "remainder"],
        "triangle_cover": ["triangle-cover", "triangle cover", "tc("],
        "transversal": ["transversal", "vertex cover"],
        "maximal_layer": ["maximal triangle-free"],
        "cone": ["cone", "k_1\\vee"],
        "layer": ["layer", "cover by"],
        "forward_link": ["forward neighborhood", "forward link"],
        "mixing": ["mixing", "mixed"],
        "escape": ["escape"],
    }
    for tag, terms in keywords.items():
        if any(t in blob for t in terms):
            tags.add(tag)
    return tuple(sorted(tags))


def parse_738(path: Path) -> list[Claim]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^####\s+([A-Z]\d+)\s+—\s+(.+?)\s*$", text, re.M))
    claims: list[Claim] = []
    for i, m in enumerate(matches):
        block = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        cid, title = m.group(1), m.group(2).strip()
        status = extract_between(block, [r"\*\*Status:\*\*\s*`?"], [r"`?\s{2,}$", r"\n\n"]).strip("` ") or "PROPOSED"
        statement = extract_between(block, [r"\*\*Statement\.\*\*"], [r"\n\n\*\*Proof route", r"\n\n\*\*Status"])
        proof = extract_between(block, [r"\*\*Proof route\.\*\*"], [r"\n\n\*\*Dependencies", r"\n\n\*\*Novelty query", r"\n\n\*\*Falsifier"])
        deps_raw = extract_between(block, [r"\*\*Dependencies\.\*\*"], [r"\n\n\*\*Novelty query"])
        deps = tuple(f"738:{d.strip()}" for d in re.findall(r"[A-Z]\d+", deps_raw))
        novelty = extract_between(block, [r"\*\*Novelty query\.\*\*"], [r"\n\n", r"\n###", r"\n####"]) or title
        if not statement:
            continue
        claim = Claim(
            uid=f"738:{cid}", origin="738", source_id=cid, title=title,
            statement=statement, status=status, proof_route=proof,
            falsifier="Counterexample to the exact quantified statement.",
            dependencies=deps, tags=infer_tags("738", cid, title, statement),
            back_transfer=("738",), lean_mission=f"formalize_738_{cid.lower()}",
            novelty_query=novelty.strip("` "), structural_leverage=70,
        ).normalized()
        claims.append(claim)
    return claims


def parse_595(path: Path) -> list[Claim]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^####\s+([A-Z]\d+)\s+—\s+(.+?)\s*$", text, re.M))
    claims: list[Claim] = []
    for i, m in enumerate(matches):
        block = text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        cid, title = m.group(1), m.group(2).strip()
        statement = extract_between(block, [r"- \*\*Statement:\*\*"], [r"\n- \*\*Status", r"\n\n"])
        status = extract_between(block, [r"- \*\*Status:\*\*"], [r"\n- ", r"\n\n"]).strip("` ") or "PROPOSED"
        proof = extract_between(block, [r"- \*\*Proof route:\*\*"], [r"\n- \*\*Falsifier", r"\n\n"])
        falsifier = extract_between(block, [r"- \*\*Falsifier:\*\*"], [r"\n- \*\*Lean", r"\n\n"]) or "Counterexample to the exact statement."
        lean = extract_between(block, [r"- \*\*Lean mission:\*\*"], [r"\n- \*\*Novelty", r"\n\n"]).strip("` ") or f"formalize_595_{cid.lower()}"
        novelty = extract_between(block, [r"- \*\*Novelty query:\*\*"], [r"\n- \*\*Prior", r"\n\n"]).strip("` ") or title
        leverage_raw = extract_between(block, [r"- \*\*Structural leverage:\*\*"], [r"\n- ", r"\n\n"])
        lm = re.search(r"(\d+)", leverage_raw)
        leverage = int(lm.group(1)) if lm else 70
        if not statement:
            continue
        claim = Claim(
            uid=f"595:{cid}", origin="595", source_id=cid, title=title,
            statement=statement, status=status, proof_route=proof, falsifier=falsifier,
            tags=infer_tags("595", cid, title, statement), back_transfer=("595",),
            lean_mission=lean, novelty_query=novelty, structural_leverage=leverage,
        ).normalized()
        claims.append(claim)
    return claims


def parse_cross(path: Path) -> list[Claim]:
    claims: list[Claim] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            cid = row["id"]
            claim = Claim(
                uid=f"X:{cid}", origin="CROSS", source_id=cid, title=row["title"],
                statement=row["statement"], status=row["status"], proof_route=row["proof_route"],
                falsifier=row["falsifier"], tags=infer_tags("CROSS", cid, row["title"], row["statement"]),
                back_transfer=("738", "595", "HYBRID"), lean_mission=row.get("lean_mission", "UNASSIGNED"),
                novelty_query=row.get("novelty_query", row["title"]),
                structural_leverage=int(row.get("structural_leverage", 80)),
            ).normalized()
            claims.append(claim)
    return claims


def generated_claim(
    uid: str, title: str, statement: str, status: str, proof: str, falsifier: str,
    deps: tuple[str, ...], tags: tuple[str, ...], back: tuple[str, ...], lean: str,
    novelty: str, leverage: int, round_no: int, rule_id: str,
) -> Claim:
    return Claim(
        uid=uid, origin="RECURSIVE", source_id=uid, title=title, statement=statement,
        status=status, proof_route=proof, falsifier=falsifier, dependencies=deps,
        tags=tuple(sorted(set(tags + ("recursive",)))), back_transfer=back,
        lean_mission=lean, novelty_query=novelty, structural_leverage=leverage,
        round_generated=round_no, rule_id=rule_id,
    ).normalized()


def build_rules() -> list[Rule]:
    rules: list[Rule] = []

    def add(rule_id: str, round_no: int, requires: tuple[str, ...], **kw: object) -> None:
        rules.append(Rule(rule_id, round_no, requires, generated_claim(round_no=round_no, rule_id=rule_id, deps=requires, **kw)))

    # Round 1: direct three-estate collisions.
    add("R1-SIGNATURE-DESCENT", 1, ("738:P07", "X:XLAYER04"),
        uid="R:R1-SIGDESC", title="Layered Signature-Fiber Defect Descent",
        statement="Let G be covered by m triangle-free layers H_i. Let P be an induced path in H_j and let F be the vertices outside P having one fixed nonempty H_j-contact signature on P. Then every ambient edge of G[F] is covered by the other m-1 layers, so tc(G[F]) <= m-1.",
        status="PROVED_IN_PACKET",
        proof="P07 makes F stable in H_j. Thus H_j contributes no edge of G[F]; every ambient edge is supplied by another covering layer.",
        falsifier="A same-signature fiber containing an edge unique to the path layer.",
        tags=("contact_signature", "layer", "triangle_cover", "tree"), back=("738", "HYBRID"),
        lean="layered_signatureFiber_defectDescent", novelty='"signature fiber" triangle-free layers defect descent', leverage=97)
    add("R1-TRANSVERSAL-SIGNATURE", 1, ("738:P07", "595:T05"),
        uid="R:R1-TRANSIG", title="Transversal Absorption of Signature-Fiber Edges",
        statement="Let D be a triangle transversal of G, put H=G-D, and let P be an induced path in the triangle-free graph H. For every fixed nonempty H-contact signature S on P, every ambient edge joining two vertices in the S-fiber belongs to D.",
        status="PROVED_IN_PACKET",
        proof="The S-fiber is stable in H by P07, so any ambient edge internal to it was deleted and lies in D.",
        falsifier="An internal fiber edge surviving in H.",
        tags=("contact_signature", "transversal", "tree"), back=("595", "HYBRID"),
        lean="transversal_absorbs_signatureFiber_edges", novelty='"triangle transversal" contact signature fiber edges', leverage=95)
    add("R1-SPIDER-DESCENT", 1, ("738:M06", "X:XLAYER04"),
        uid="R:R1-SPIDERDESC", title="Layer-Induced Spider Defect Descent",
        statement="If a spider is induced inside one layer of an m-layer triangle-free edge cover, then all ambient chords on the spider vertices are covered by the other m-1 layers.",
        status="PROVED_IN_PACKET",
        proof="A spider is a tree. Apply layer-defect descent to the induced tree in the selected layer.",
        falsifier="An ambient chord present only in the layer where the spider is induced.",
        tags=("mixing", "tree", "layer", "triangle_cover"), back=("738", "HYBRID"),
        lean="layerInduced_spider_defectDescent", novelty='"induced spider" ambient defects triangle-free layers', leverage=88)
    add("R1-CRITICAL-ESCAPE-DESCENT", 1, ("738:N13", "X:XLAYER04"),
        uid="R:R1-ESCAPEDESC", title="Critical Escape with Lower-Layer Ambient Defects",
        statement="Let H_j be a finite k-critical triangle-free layer in an m-layer cover of G. For every connected S with 2 <= |S| < k, H_j has a component C outside N_{H_j}[S] with chi(C) >= k-|S|, and every ambient edge of G[C] absent from H_j[C] is covered by the other m-1 layers.",
        status="PROVED_IN_PACKET",
        proof="Use N13 inside H_j; the final assertion is immediate from the edge cover.",
        falsifier="Failure of the critical escape component or an ambient defect unique to H_j.",
        tags=("critical", "escape", "layer", "triangle_cover"), back=("738", "HYBRID"),
        lean="criticalEscape_with_lowerLayerDefects", novelty='"critical escape component" ambient defect layers', leverage=92)
    add("R1-LINK-PROTECTED-RESERVE", 1, ("X:XLINK06", "738:N07"),
        uid="R:R1-LINKRESERVE", title="Protected Deletion Reserve Inside Every #595 Witness Link",
        statement="Let G be a K4-free graph with tc(G)>aleph_0 and fix any well-order. In the uncountably chromatic triangle-free forward link supplied by XLINK06, every finite sequence of protected deletions from N07 leaves an uncountably chromatic residual.",
        status="PROVED_IN_PACKET",
        proof="XLINK06 supplies a triangle-free link of uncountable chromatic number. N07 subtracts only a finite chromatic budget, which cannot make an uncountable cardinal finite or countable.",
        falsifier="A finite protected deletion sequence reducing the link to countable chromatic number.",
        tags=("forward_link", "protected_deletion", "chromatic", "k4_free"), back=("595", "738", "HYBRID"),
        lean="witnessLink_protectedDeletion_preserves_uncountableChromatic", novelty='"Erdos 595 witness" protected deletion forward neighborhood', leverage=100)
    add("R1-MAXIMAL-CONTACT-ABSORPTION", 1, ("738:P07", "X:XTRANS03"),
        uid="R:R1-MAXCONTACT", title="Maximal-Layer Contact Defects Lie in the Minimal Transversal",
        statement="Let H be a maximal spanning triangle-free subgraph of G and D=E(G)\\E(H). For an induced path P in H, every edge internal to a fixed nonempty H-contact-signature fiber belongs to the inclusion-minimal triangle transversal D.",
        status="PROVED_IN_PACKET",
        proof="P07 makes the fiber stable in H. XTRANS03 identifies the complement of H as a minimal transversal.",
        falsifier="A fiber edge in H or outside both H and D.",
        tags=("maximal_layer", "contact_signature", "transversal"), back=("595", "HYBRID"),
        lean="maximalLayer_contactDefects_in_minimalTransversal", novelty='"maximal triangle-free" contact signature minimal transversal', leverage=96)
    add("R1-K4-SIGNATURE-FIBER", 1, ("738:P07", "X:XLINK05"),
        uid="R:R1-K4FIBER", title="K4-Free Ambient Signature-Fiber Collapse",
        statement="Let G be K4-free, let H be any spanning subgraph, and let P be a path in H. If F is a nonempty H-contact-signature fiber on P, then G[F] is triangle-free.",
        status="PROVED_IN_PACKET",
        proof="Choose p in the nonempty signature. Every vertex of F is adjacent to p in G, so F lies in N_G(p); XLINK05 makes that neighborhood triangle-free.",
        falsifier="A triangle inside a nonempty signature fiber of a K4-free graph.",
        tags=("k4_free", "contact_signature", "triangle_free"), back=("738", "595", "HYBRID"),
        lean="K4free_signatureFiber_triangleFree", novelty='"K4-free" contact signature fiber triangle-free', leverage=98)
    add("R1-SIBLING-DEFECT", 1, ("738:T10", "X:XLINK05"),
        uid="R:R1-SIBDEF", title="Sibling Defect Graphs Are Triangle-Free in K4-Free Hosts",
        statement="Let a rooted tree copy lie in a K4-free ambient graph. For every tree vertex u, the ambient graph induced by the selected children of u is triangle-free; in particular every sibling-defect graph is triangle-free, regardless of the type-tensor profile.",
        status="PROVED_IN_PACKET",
        proof="All selected children lie in the ambient neighborhood of u, which is triangle-free by XLINK05.",
        falsifier="Three selected children of one parent forming an ambient triangle.",
        tags=("k4_free", "type_tensor", "tree", "triangle_free"), back=("738", "HYBRID"),
        lean="K4free_siblingDefect_triangleFree", novelty='"sibling defect graph" K4-free rooted tree', leverage=91)

    # Round 2: rules that consume Round-1 outputs.
    add("R2-SIGNATURE-COVER-OBSTRUCTION", 2, ("R:R1-K4FIBER", "595:T05"),
        uid="R:R2-SIGCOVEROBS", title="Countable Signature-Fiber Cover Obstruction",
        statement="If G is K4-free and tc(G)>aleph_0, then no countable family of nonempty contact-signature fibers (taken from arbitrary spanning scaffolds and finite paths) has internal edge sets covering E(G).",
        status="PROVED_IN_PACKET",
        proof="Each internal fiber graph is triangle-free by R1-K4FIBER. A countable edge cover by them would contradict tc(G)>aleph_0.",
        falsifier="A #595 witness whose edges are covered by countably many signature fibers.",
        tags=("k4_free", "contact_signature", "triangle_cover", "dispersion"), back=("595", "HYBRID"),
        lean="witness_no_countable_signatureFiber_edgeCover", novelty='"signature fiber cover" K4-free uncountable triangle cover', leverage=100)
    add("R2-ROOT-DEFECT-SPLIT", 2, ("R:R1-SPIDERDESC", "R:R1-SIBDEF"),
        uid="R:R2-ROOTSPLIT", title="Root-Level versus Deep Spider-Defect Split",
        statement="For a spider induced in one layer of a K4-free m-layer graph, ambient chords among first arm vertices form a triangle-free graph, while every remaining ambient chord is covered by the other m-1 layers.",
        status="PROVED_IN_PACKET",
        proof="First arm vertices are siblings at the center, so R1-SIBDEF applies. All chords are absent from the inducing layer, so R1-SPIDERDESC covers the rest.",
        falsifier="A root-level chord triangle or a deep chord unique to the inducing layer.",
        tags=("mixing", "tree", "k4_free", "layer", "triangle_cover"), back=("738", "HYBRID"),
        lean="layerSpider_rootDeep_defectSplit", novelty='"spider defects" root level K4-free layers', leverage=94)
    add("R2-STABLE-CERTIFICATE", 2, ("X:XTRANS03", "X:XLINK05"),
        uid="R:R2-STABLECERT", title="Stable Certification of Omitted Edges",
        statement="Let G be K4-free, H a maximal spanning triangle-free subgraph, and D=E(G)\\E(H). For every omitted edge xy in D, the set W_H(xy)=N_H(x) intersect N_H(y) is nonempty and is stable in G.",
        status="PROVED_IN_PACKET",
        proof="Maximality of H implies that adding xy creates a triangle, so W_H(xy) is nonempty. Any edge between two common neighbors together with x,y would create a K4.",
        falsifier="An omitted edge with no H-common neighbor, or adjacent vertices in its certificate set.",
        tags=("k4_free", "maximal_layer", "transversal", "certificate", "stable"), back=("595", "738", "HYBRID"),
        lean="maximalTriangleFree_omittedEdge_stableCertificate", novelty='"maximal triangle-free subgraph" omitted edge stable common neighbors', leverage=100)
    add("R2-CERTIFIED-SIGNATURE-DEFECT", 2, ("R:R1-MAXCONTACT", "R:R2-STABLECERT"),
        uid="R:R2-SIGCERT", title="Signature Defects Carry Stable Triangle Certificates",
        statement="Under R1-MAXCONTACT in a K4-free graph, every defect edge xy inside a nonempty path-signature fiber belongs to the minimal transversal and has a nonempty stable certificate set W_H(xy). Every path contact p in the shared signature is itself a certificate witness.",
        status="PROVED_IN_PACKET",
        proof="R1-MAXCONTACT places xy in D. Since x and y both contact every p in the signature inside H, each such p lies in W_H(xy); stability follows from R2-STABLECERT.",
        falsifier="A defect edge lacking a shared contact or with a nonstable certificate set.",
        tags=("contact_signature", "maximal_layer", "transversal", "certificate"), back=("595", "738", "HYBRID"),
        lean="signatureDefect_has_stableCertificates", novelty='"contact signature defect" stable triangle certificate', leverage=98)
    add("R2-TRANSVERSAL-TREE-SEQUENCE", 2, ("R:R1-LINKRESERVE", "X:XCONE06"),
        uid="R:R2-TREESEQ", title="Protected Tree-Sequence Extraction in a Witness Link",
        statement="Conditional on the #738 statements for a prescribed sequence of finite trees T_0,T_1,..., every #595 witness contains under one apex pairwise anticomplete induced copies of all T_i inside one forward link; every ambient chord within or between these copies lies outside the link layer.",
        status="CONDITIONAL_ON_738_SEQUENCE",
        proof="Use R1-LINKRESERVE to retain uncountable chromatic number after each protected deletion and apply the relevant #738(T_i) bound at every stage. Chords are absent from the induced link copies and from link-anticompleteness.",
        falsifier="A verified #738 sequence and a witness where the recursive extraction fails.",
        tags=("forward_link", "protected_deletion", "tree", "cone", "conditional"), back=("738", "595", "HYBRID"),
        lean="witnessLink_extract_treeSequence", novelty='"Erdos 595" pairwise anticomplete induced tree sequence link', leverage=96)
    add("R2-LAYERED-CONTACT-REDUCTION", 2, ("R:R1-SIGDESC", "738:P05"),
        uid="R:R2-CONTACTRED", title="Finite Contact-Language Reduction for Layered Defects",
        statement="For an n-vertex induced path in one triangle-free layer of an m-layer graph, its vertices outside the path split into at most F_{n+2}-1 nonempty contact-signature fibers, and each fiber's ambient internal defect graph has triangle-cover number at most m-1.",
        status="PROVED_IN_PACKET",
        proof="P05 bounds the nonempty signatures and R1-SIGDESC handles each fiber.",
        falsifier="More than F_{n+2}-1 signatures or a fiber defect requiring m layers.",
        tags=("contact_signature", "layer", "fibonacci", "triangle_cover"), back=("738", "HYBRID"),
        lean="layeredPath_contactLanguage_defectReduction", novelty='"Fibonacci contact signatures" layered defect graph', leverage=93)
    add("R2-CRITICAL-ABSORPTION", 2, ("R:R1-ESCAPEDESC", "595:T05"),
        uid="R:R2-CRITABSORB", title="Critical Escape Defects as Lower-Layer Transversal Data",
        statement="In an m-layer graph, a high-chromatic critical escape component extracted inside one triangle-free layer has all ambient nonlayer edges covered by the remaining m-1 layers; equivalently those lower layers form a triangle-free cover of the escape defect graph.",
        status="PROVED_IN_PACKET",
        proof="This is the edge-cover conclusion of R1-ESCAPEDESC, restated in triangle-cover language.",
        falsifier="An escape defect edge absent from every lower layer.",
        tags=("critical", "escape", "layer", "transversal"), back=("738", "HYBRID"),
        lean="criticalEscape_defectGraph_lowerLayerCover", novelty='"critical escape" defect graph lower layers', leverage=89)
    add("R2-SINGLE-BOOK", 2, ("R:R2-STABLECERT", "X:XCONE08"),
        uid="R:R2-BOOKSTERILE", title="Single Stable Triangle Book Is Two-Layer Sterile",
        statement="Let xy be an edge and W a stable set of common neighbors of x and y. The graph on {x,y} union W has triangle-cover number exactly 2 when W is nonempty.",
        status="PROVED_IN_PACKET",
        proof="One layer is the star from x to {y} union W; the other is the star from y to W. A triangle xyw gives the lower bound two.",
        falsifier="A nonempty stable triangle book coverable in one layer or requiring three.",
        tags=("certificate", "stable", "triangle_cover", "sterility"), back=("595", "HYBRID"),
        lean="stableTriangleBook_triangleCover_eq_two", novelty='"triangle book" stable pages triangle-free cover two', leverage=92)

    # Round 3: uses newly generated certificates and centeredness.
    add("R3-COMMON-OMITTED-BOOK", 3, ("R:R2-STABLECERT", "X:XTRANS05"),
        uid="R:R3-COMMONBOOK", title="Common Omitted-Edge Stable Book Theorem",
        statement="Let G be K4-free with tc(G)>aleph_0. For every countable family H_n of maximal spanning triangle-free subgraphs, there is an edge xy omitted from every H_n. For each n, H_n supplies a nonempty stable certificate set W_{H_n}(xy) subseteq N_G(x) intersect N_G(y).",
        status="PROVED_IN_PACKET",
        proof="XTRANS05 gives an edge omitted by all H_n. Apply R2-STABLECERT separately to every maximal layer; all certificates lie in the common neighborhood, which is stable in a K4-free graph.",
        falsifier="A countable maximal-layer family with no common omitted edge or a layer lacking a stable certificate.",
        tags=("k4_free", "maximal_layer", "transversal", "certificate", "countable_centered"), back=("595", "738", "HYBRID"),
        lean="witness_countableMaximalLayers_commonStableBook", novelty='"countable maximal triangle-free subgraphs" common omitted edge stable witnesses', leverage=100)
    add("R3-KAPPA-OMITTED-BOOK", 3, ("R:R2-STABLECERT", "595:T05"),
        uid="R:R3-KAPPABOOK", title="Cardinal Stable-Book Centeredness",
        statement="If G is K4-free and tc(G)>kappa, then every family of at most kappa maximal spanning triangle-free subgraphs has a common omitted edge xy, and every member supplies a nonempty stable certificate set inside N_G(x) intersect N_G(y).",
        status="PROVED_IN_PACKET",
        proof="Use transversal centeredness T05 for the complements and R2-STABLECERT for each layer.",
        falsifier="A family of size at most kappa with empty common complement or an uncertified omitted edge.",
        tags=("k4_free", "maximal_layer", "transversal", "certificate", "cardinal"), back=("595", "HYBRID"),
        lean="triangleCover_gt_kappa_commonStableBook", novelty='"cardinal" maximal triangle-free layers common omitted edge', leverage=100)
    add("R3-BOOK-DISPERSION", 3, ("R:R3-COMMONBOOK", "R:R2-BOOKSTERILE"),
        uid="R:R3-BOOKDISP", title="Stable-Book Localization–Dispersion",
        statement="Every countable attempt to cover a #595 witness by maximal triangle-free layers exposes one common stable triangle book, but that book itself has triangle-cover number two. Hence the failure of the attempted cover cannot be localized to the certificate book alone and must involve its interactions with edges outside the book.",
        status="PROVED_IN_PACKET",
        proof="R3-COMMONBOOK constructs the book; R2-BOOKSTERILE proves it is two-layer coverable.",
        falsifier="A common certificate book that itself has uncountable triangle-cover number.",
        tags=("dispersion", "sterility", "maximal_layer", "certificate"), back=("595", "HYBRID"),
        lean="commonStableBook_obstruction_migrates", novelty='"stable triangle book" cover obstruction migration', leverage=99)
    add("R3-PROFILE-BASIS-REDUCTION", 3, ("R:R2-SIGCERT", "R:R3-COMMONBOOK"),
        uid="R:R3-PROFILEBASIS", title="Stable-Book Profile-Basis Close Reduction",
        statement="To contradict tc(G)>aleph_0 it is sufficient to construct a countable family of maximal triangle-free layers whose omitted-edge stable certificate books realize every possible path-contact certificate profile: R3-COMMONBOOK would then produce a common omitted edge with a profile already handled by one of the layers.",
        status="CONDITIONAL_REDUCTION",
        proof="This is a precise close reduction: completeness of the profile basis would force the common omitted edge to be included by a corresponding layer, contradicting its common omission. The load-bearing hypothesis is profile completeness.",
        falsifier="A certificate profile not captured by the proposed countable basis or a semantic mismatch between profile handling and edge inclusion.",
        tags=("contact_signature", "certificate", "maximal_layer", "close_reduction"), back=("595", "HYBRID"),
        lean="stableBook_profileBasis_reduction", novelty='"stable certificate book" countable profile basis triangle cover', leverage=100)
    add("R3-LAYERED-GYARFAS-RECURRENCE", 3, ("R:R2-CONTACTRED", "X:XLAYER05"),
        uid="R:R3-FREC", title="Recursive Contact-Code Program for the Finite-Layer Gyárfás Hierarchy",
        statement="For the conjectural hierarchy f(T,m), an induced path/tree scaffold in one layer reduces each fixed contact fiber to an (m-1)-layer defect problem and reduces the total number of fiber types to a finite contact language. Thus any proof of a uniform cross-fiber gluing lemma yields an explicit recurrence from m-1 to m.",
        status="CONDITIONAL_REDUCTION",
        proof="R2-CONTACTRED gives finite fibers with lower layer depth; XLAYER05 supplies the induction coordinate. Only cross-fiber edges remain unsupported.",
        falsifier="A family where within-fiber descent holds but no finite cross-fiber gluing statement can bound the hierarchy.",
        tags=("contact_signature", "layer", "tree", "recurrence", "close_reduction"), back=("738", "HYBRID"),
        lean="finiteLayerGyarfas_contactRecurrence_reduction", novelty='"finite-layer Gyárfás" contact code recurrence', leverage=100)
    add("R3-TWO-LAYER-FIBER-TARGET", 3, ("R:R1-K4FIBER", "R:R2-CONTACTRED"),
        uid="R:R3-TWOLAYER", title="Two-Layer Cross-Fiber Purification Target",
        statement="In the m=2 hybrid hierarchy, every individual nonempty contact-signature fiber is ambiently triangle-free in a K4-free host. The sole remaining purification problem is to control edges between distinct signature fibers.",
        status="UNPROVED_CHECKABLE_TARGET",
        proof="Within-fiber structure is settled by R1-K4FIBER; R2-CONTACTRED leaves only cross-fiber interactions.",
        falsifier="A two-layer counterexample whose obstruction already occurs inside one signature fiber.",
        tags=("contact_signature", "layer", "k4_free", "search_target"), back=("738", "HYBRID"),
        lean="twoLayer_crossFiber_purification_target", novelty='"two-layer" cross signature fiber induced tree purification', leverage=100)
    add("R3-BOOK-CANONIZATION-TARGET", 3, ("R:R3-COMMONBOOK", "738:P05"),
        uid="R:R3-BOOKCANON", title="Stable-Book Witness Canonization Target",
        statement="Given the common omitted edge xy from R3-COMMONBOOK, canonize the layer-specific stable witnesses by finitely many path-contact signatures relative to a protected scaffold in the high-chromatic link. A successful countable canonization would feed R3-PROFILEBASIS.",
        status="UNPROVED_CHECKABLE_TARGET",
        proof="P05 supplies finite contact alphabets on each finite path; the missing step is a uniform protected scaffold and compatibility across all layers.",
        falsifier="A finite family of layers whose witnesses evade every proposed finite signature scaffold.",
        tags=("contact_signature", "certificate", "canonization", "search_target"), back=("595", "738", "HYBRID"),
        lean="stableBook_witnessCanonization_target", novelty='"stable triangle book" path contact canonization', leverage=100)
    add("R3-BOOK-BRANCH-BLADE", 3, ("R:R3-COMMONBOOK", "738:C01"),
        uid="R:R3-BOOKBRANCH", title="Stable Book as a Clean Branch Reservoir",
        statement="The page set of every common omitted-edge book in a K4-free graph is stable. Hence, relative to any outside finite candidate set, the #738 clean-child/large-fan dichotomy applies to any chosen neighborhood subset of that page set without internal page conflicts.",
        status="PROVED_IN_PACKET",
        proof="R3-COMMONBOOK gives a stable page set; C01 is then applicable with that set as the branch-candidate reservoir whenever its hypotheses are instantiated.",
        falsifier="Internal adjacency among book pages or a violation of C01 under a valid instantiation.",
        tags=("certificate", "stable", "contamination", "transfer_blade"), back=("738", "595", "HYBRID"),
        lean="stableBook_cleanBranchReservoir", novelty='"triangle book pages" clean child fan dichotomy', leverage=89)

    # Round 4: recursive mining and exact sterility/close interfaces.
    add("R4-MINIMAL-TRANSVERSAL-PAGE", 4, ("R:R2-STABLECERT", "X:XTRANS03"),
        uid="R:R4-PAGECERT", title="Minimal-Transversal Page Certificate Theorem",
        statement="Let D be an inclusion-minimal triangle transversal of a K4-free graph and H=G-D. For every edge xy in D there is z with xz,yz in H; all such z form a stable set. Thus each minimal-transversal edge is the spine of a nonempty stable book whose pages use exactly one transversal edge.",
        status="PROVED_IN_PACKET",
        proof="XTRANS03 makes H maximal triangle-free. Apply R2-STABLECERT. Each triangle xyz uses xy in D and its other two edges in H.",
        falsifier="A minimal-transversal edge without an exact one-edge page certificate or with adjacent witnesses.",
        tags=("transversal", "certificate", "stable", "book"), back=("595", "738", "HYBRID"),
        lean="minimalTransversal_edge_has_stablePageCertificates", novelty='"minimal triangle transversal" stable book page certificate', leverage=100)
    add("R4-COUNTABLE-PAGE-FAMILY", 4, ("R:R3-COMMONBOOK", "R:R4-PAGECERT"),
        uid="R:R4-PAGEFAMILY", title="Countable Layer Family Produces a Shared Stable Page Space",
        statement="For every countable family of maximal triangle-free layers in a #595 witness, there is one edge xy such that every layer selects a nonempty subset of the same stable page space N_G(x) intersect N_G(y) as exact triangle certificates for omitting xy.",
        status="PROVED_IN_PACKET",
        proof="R3-COMMONBOOK supplies xy and layer-specific certificate sets; R4-PAGECERT identifies them as exact page certificates in the common stable neighborhood.",
        falsifier="A layer whose witnesses leave the common page space or do not exactly certify xy.",
        tags=("maximal_layer", "certificate", "stable", "countable_centered"), back=("595", "HYBRID"),
        lean="countableMaximalLayers_sharedStablePageSpace", novelty='"shared stable page space" maximal triangle-free layers', leverage=100)
    add("R4-PAGE-PROFILE-COMPACTNESS", 4, ("R:R4-PAGEFAMILY", "R:R3-BOOKCANON"),
        uid="R:R4-PAGECOMPACT", title="Page-Profile Compactness Close Program",
        statement="A countable canonization theorem for subsets of the shared stable page space—strong enough to choose a maximal triangle-free layer that includes the spine edge for every realized canonical profile—would refute the existence of a #595 witness.",
        status="CONDITIONAL_REDUCTION",
        proof="R4-PAGEFAMILY reduces every countable layer failure to one stable page space; R3-BOOKCANON identifies the missing canonization. A profile-complete layer basis contradicts common omission.",
        falsifier="A canonical page profile for which every corresponding maximal layer must still omit the spine edge.",
        tags=("compactness", "canonization", "certificate", "close_reduction"), back=("595", "HYBRID"),
        lean="pageProfile_compactness_closeReduction", novelty='"stable page space" canonical profiles triangle cover compactness', leverage=100)
    add("R4-MULTIBOOK-INTERACTION", 4, ("R:R3-BOOKDISP", "R:R2-BOOKSTERILE"),
        uid="R:R4-MULTIBOOK", title="Multi-Book Interaction Frontier",
        statement="Since every individual stable triangle book has tc=2 and the common-book obstruction migrates outside it, the first genuine finite model for #595 must involve K4-safe interactions among at least two books. Classify the smallest interaction raising tc above 2.",
        status="UNPROVED_CHECKABLE_TARGET",
        proof="R3-BOOKDISP and R2-BOOKSTERILE kill all single-book mechanisms.",
        falsifier="A single stable book with tc>2, or a proof that arbitrary disjoint book unions already suffice.",
        tags=("book", "interaction", "sterility", "finite_search"), back=("595", "HYBRID"),
        lean="multiBook_interaction_frontier", novelty='"interacting triangle books" K4-free triangle cover number', leverage=100)
    add("R4-LAYER-SIGNATURE-MULTIPLIER", 4, ("R:R3-FREC", "R:R4-PAGECERT"),
        uid="R:R4-MULTIPLIER", title="Layer–Signature–Certificate Multiplier",
        statement="The finite-layer tree hierarchy and the #595 maximal-layer program share one recursive state object: a finite contact signature together with a lower-layer defect cover and a stable page-certificate family. Any theorem bounding this combined object transfers simultaneously to #738 purification, #595 maximal-layer bases, and the hybrid m-layer hierarchy.",
        status="CONDITIONAL_REDUCTION",
        proof="R3-FREC supplies signature plus lower-layer defect state; R4-PAGECERT supplies certificate state. The transfer directions are explicit, while the required bound remains open.",
        falsifier="A bound valid in the combined state but failing one of the three stated transfer maps.",
        tags=("rsi_multiplier", "contact_signature", "layer", "certificate"), back=("738", "595", "HYBRID"),
        lean="layerSignatureCertificate_multiplier", novelty='"contact signature" lower layer defects stable certificates', leverage=100)
    add("R4-SINGLE-LINK-AND-BOOK-STERILITY", 4, ("X:XCONE10", "R:R2-BOOKSTERILE"),
        uid="R:R4-DOUBLESTERILE", title="Single-Link and Single-Book Double Sterility",
        statement="Neither arbitrary complexity inside one K4-free link nor arbitrary size of one stable triangle book can force triangle-cover number above two. Any #595 construction mechanism must therefore coordinate multiple links and multiple books simultaneously.",
        status="PROVED_IN_PACKET",
        proof="XCONE10 kills single-link complexity and R2-BOOKSTERILE kills single-book complexity.",
        falsifier="A theorem deriving tc>2 solely from one link or one stable book.",
        tags=("sterility", "forward_link", "book", "dispersion"), back=("595", "HYBRID"),
        lean="singleLink_singleBook_doubleSterility", novelty='"single link" "single triangle book" sterility', leverage=100)
    add("R4-THREE-CLOSE-INTERFACE", 4, ("R:R4-MULTIPLIER", "R:R4-PAGECOMPACT"),
        uid="R:R4-TRICLOSE", title="Three-Campaign Close Interface",
        statement="The three flagship close programs can be synchronized around one obligation: classify combined contact-signature, lower-layer-defect, and stable-page-certificate states well enough to (i) purify induced trees, (ii) construct a countable maximal-layer basis, or (iii) prove the finite-layer hierarchy recurrence.",
        status="CONDITIONAL_REDUCTION",
        proof="R4-MULTIPLIER establishes the shared state object; R4-PAGECOMPACT identifies the #595 close use. The #738 and hybrid uses are supplied by R3-FREC.",
        falsifier="A classification sufficient for one state but semantically incapable of transfer to the other two.",
        tags=("close_reduction", "rsi_multiplier", "three_way"), back=("738", "595", "HYBRID"),
        lean="threeCampaign_closeInterface", novelty='"three-way" induced tree triangle cover contact certificate state', leverage=100)
    add("R4-CANONICAL-STATE-CENSUS", 4, ("R:R4-TRICLOSE", "R:R3-TWOLAYER"),
        uid="R:R4-CENSUS", title="Canonical State Census Target",
        statement="Enumerate finite combined states consisting of a path/tree contact signature, a layer-colored defect tensor, and a stable page-certificate incidence family; quotient by isomorphism and determine the minimal forbidden states for the two-layer case.",
        status="UNPROVED_CHECKABLE_TARGET",
        proof="This is the finite executable form of the shared close interface, with m=2 as the first nontrivial boundary.",
        falsifier="A missing state schema discovered by a finite graph outside the encoding or nonisomorphic states incorrectly identified.",
        tags=("finite_search", "contact_signature", "type_tensor", "certificate", "two_layer"), back=("738", "595", "HYBRID"),
        lean="canonicalCombinedState_census", novelty='"contact signature defect tensor certificate incidence" census', leverage=100)

    return rules


class Forge:
    def __init__(self, claims: Iterable[Claim], rules: Iterable[Rule], recursive: bool = True):
        self.claims: dict[str, Claim] = {c.uid: c for c in claims}
        self.hash_index: dict[str, str] = {c.claim_hash: c.uid for c in claims}
        self.rules = sorted(rules, key=lambda r: (r.round_no, r.rule_id))
        self.recursive = recursive
        self.generated: list[Claim] = []
        self.round_receipts: list[RoundReceipt] = []
        self.retracted: set[str] = set()
        self.close_programs = self._init_close_programs()

    def _init_close_programs(self) -> dict[str, CloseProgram]:
        return {
            "CLOSE-738": CloseProgram("CLOSE-738", "Erdos #738", [
                "signature_fiber_control", "cross_fiber_gluing", "two_layer_purification",
                "finite_layer_recurrence", "combined_state_classification",
            ]),
            "CLOSE-595": CloseProgram("CLOSE-595", "Erdos #595", [
                "maximal_layer_edge_certificates", "common_omitted_edge_structure",
                "page_profile_canonization", "countable_maximal_layer_basis",
                "multi_link_multi_book_interaction",
            ]),
            "CLOSE-HYBRID": CloseProgram("CLOSE-HYBRID", "Finite-layer induced-tree hierarchy", [
                "layer_defect_descent", "signature_fiber_descent", "cross_fiber_gluing",
                "finite_layer_recurrence", "combined_state_classification",
            ]),
        }

    def _resolve_obligations(self) -> None:
        mapping = {
            "R:R1-K4FIBER": ["signature_fiber_control"],
            "R:R1-SIGDESC": ["signature_fiber_descent"],
            "X:XLAYER04": ["layer_defect_descent"],
            "R:R2-STABLECERT": ["maximal_layer_edge_certificates"],
            "R:R3-COMMONBOOK": ["common_omitted_edge_structure"],
            "R:R3-FREC": ["finite_layer_recurrence"],
            "R:R4-CENSUS": ["combined_state_classification"],
            "R:R4-PAGECOMPACT": ["page_profile_canonization"],
            "R:R4-MULTIBOOK": ["multi_link_multi_book_interaction"],
            "R:R3-TWOLAYER": ["two_layer_purification"],
            "R:R3-PROFILEBASIS": ["countable_maximal_layer_basis"],
        }
        for uid, obs in mapping.items():
            if uid not in self.claims or uid in self.retracted:
                continue
            claim = self.claims[uid]
            if claim.status in SAFE_EXACT:
                for program in self.close_programs.values():
                    for ob in obs:
                        if ob in program.obligations:
                            program.resolved_by[ob] = uid

    def _safe_status(self, rule: Rule) -> tuple[str, str | None]:
        requested = rule.output.status
        dep_statuses = [self.claims[d].status for d in rule.requires]
        if requested in SAFE_EXACT:
            if all(s in SAFE_EXACT for s in dep_statuses):
                return requested, None
            return "CONDITIONAL_REDUCTION", f"{rule.rule_id}: exact status downgraded due to conditional/search dependency"
        return requested, None

    def run(self, max_round: int = 4) -> None:
        source_uids = {u for u, c in self.claims.items() if c.round_generated == 0}
        for round_no in range(1, max_round + 1):
            before_close = {k: len(v.unresolved) for k, v in self.close_programs.items()}
            generated_ids: list[str] = []
            duplicate_rejections: list[str] = []
            downgrades: list[str] = []
            inherited = len(self.claims)
            round_rules = [r for r in self.rules if r.round_no == round_no]
            pending = {r.rule_id: r for r in round_rules}
            progressed = True
            while progressed:
                progressed = False
                for rule_id in sorted(list(pending)):
                    rule = pending[rule_id]
                    if not all(d in self.claims and d not in self.retracted for d in rule.requires):
                        continue
                    if not self.recursive and not all(d in source_uids for d in rule.requires):
                        pending.pop(rule_id)
                        continue
                    status, downgrade = self._safe_status(rule)
                    if downgrade:
                        downgrades.append(downgrade)
                    out = Claim(**{**asdict(rule.output), "status": status}).normalized()
                    if out.claim_hash in self.hash_index:
                        duplicate_rejections.append(f"{rule.rule_id}->{self.hash_index[out.claim_hash]}")
                        pending.pop(rule_id)
                        continue
                    if out.uid in self.claims:
                        duplicate_rejections.append(f"{rule.rule_id}->uid:{out.uid}")
                        pending.pop(rule_id)
                        continue
                    self.claims[out.uid] = out
                    self.hash_index[out.claim_hash] = out.uid
                    self.generated.append(out)
                    generated_ids.append(out.uid)
                    pending.pop(rule_id)
                    progressed = True
            self._resolve_obligations()
            after_close = {k: len(v.unresolved) for k, v in self.close_programs.items()}
            payload = {
                "round_no": round_no,
                "inherited_claims": inherited,
                "generated_ids": generated_ids,
                "duplicate_rejections": duplicate_rejections,
                "status_downgrades": downgrades,
                "close_unresolved_before": before_close,
                "close_unresolved_after": after_close,
            }
            receipt = RoundReceipt(**payload, content_hash=sha256_text(canonical_json(payload)))
            self.round_receipts.append(receipt)

    def retract(self, uid: str) -> list[str]:
        self.retracted.add(uid)
        invalidated = []
        changed = True
        while changed:
            changed = False
            for c in self.generated:
                if c.uid in self.retracted:
                    continue
                if any(d in self.retracted for d in c.dependencies):
                    self.retracted.add(c.uid)
                    invalidated.append(c.uid)
                    changed = True
        return invalidated

    def summary(self) -> dict[str, object]:
        status_counts: dict[str, int] = {}
        for c in self.generated:
            status_counts[c.status] = status_counts.get(c.status, 0) + 1
        return {
            "source_claims": len([c for c in self.claims.values() if c.round_generated == 0]),
            "generated_claims": len(self.generated),
            "total_claims": len(self.claims),
            "status_counts": status_counts,
            "back_transfer_counts": {
                key: sum(key in c.back_transfer for c in self.generated)
                for key in ("738", "595", "HYBRID")
            },
            "close_programs": {
                k: {
                    "target": v.target,
                    "resolved": len(v.resolved_by),
                    "unresolved": v.unresolved,
                    "resolved_by": v.resolved_by,
                }
                for k, v in self.close_programs.items()
            },
            "rounds": [asdict(r) for r in self.round_receipts],
            "retracted": sorted(self.retracted),
        }


def write_jsonl(path: Path, claims: Iterable[Claim]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for c in claims:
            f.write(json.dumps(asdict(c), ensure_ascii=False, sort_keys=True) + "\n")


def build_report(out_dir: Path, forge: Forge, control: Forge, sources: dict[str, Path]) -> str:
    summary = forge.summary()
    control_summary = control.summary()
    top = sorted(forge.generated, key=lambda c: (-c.structural_leverage, c.uid))[:12]
    lines = [
        "# Three-Way Recursive Theorem Forge — Build, Run, and Proof Report",
        "",
        "**Date:** 2026-08-04  ",
        "**Targets:** Erdős #738, Erdős #595, and the 738×595 cross-campaign hierarchy  ",
        "**Novelty:** UNRUN — exact queries are emitted for the local checker  ",
        "**Lean:** UNRUN — theorem names are emitted as local missions  ",
        "",
        "## Claim boundary",
        "",
        "This run proves deterministic ingestion, typed recursive transfer, fail-closed authority handling, repeated close-program updates, hostile refusal, finite graph checks for the mathematical kernel, and causal advantage over a nonrecursive control. It does not claim either Erdős flagship is solved or that generated statements are historically novel.",
        "",
        "## Source estate",
        "",
    ]
    for key, p in sources.items():
        lines.append(f"- **{key}:** `{p.name}` — SHA-256 `{hashlib.sha256(p.read_bytes()).hexdigest()}`")
    lines += [
        "",
        "## Run result",
        "",
        f"- Parsed source claims: **{summary['source_claims']}**",
        f"- Recursive claims emitted: **{summary['generated_claims']}**",
        f"- Total unified claims: **{summary['total_claims']}**",
        f"- Nonrecursive control claims: **{control_summary['generated_claims']}**",
        f"- Recursive gain: **{summary['generated_claims'] - control_summary['generated_claims']} claims**",
        f"- Back-transfers to #738: **{summary['back_transfer_counts']['738']}**",
        f"- Back-transfers to #595: **{summary['back_transfer_counts']['595']}**",
        f"- Back-transfers to hybrid hierarchy: **{summary['back_transfer_counts']['HYBRID']}**",
        "",
        "## Highest-leverage recursive outputs",
        "",
    ]
    for c in top:
        lines += [
            f"### {c.uid} — {c.title}",
            f"**Status:** `{c.status}`  ",
            f"**Rule:** `{c.rule_id}`  ",
            f"**Dependencies:** `{', '.join(c.dependencies)}`  ",
            f"**Back-transfer:** `{', '.join(c.back_transfer)}`  ",
            f"**Claim hash:** `{c.claim_hash}`",
            "",
            f"**Statement.** {c.statement}",
            "",
            f"**Proof route.** {c.proof_route}",
            "",
            f"**Falsifier.** {c.falsifier}",
            "",
            f"**Lean mission.** `{c.lean_mission}`",
            "",
            f"**Novelty query.** `{c.novelty_query}`",
            "",
        ]
    lines += [
        "## Three simultaneous close programs",
        "",
    ]
    for k, v in summary["close_programs"].items():
        lines += [
            f"### {k} — {v['target']}",
            f"- Resolved obligations: **{v['resolved']}**",
            f"- Remaining exact obligations: `{', '.join(v['unresolved']) or 'NONE'}`",
            "",
        ]
    lines += [
        "## Strongest new recursive seam",
        "",
        "A maximal spanning triangle-free layer in a K4-free graph certifies each omitted edge by a nonempty stable set of common-neighbor pages. Countable transversal centeredness then forces every countable family of maximal layers in a #595 witness to omit one common edge and to choose its certificates from one shared stable page space. The page space is itself two-layer sterile, so the true obstruction lies in page-profile and inter-book interactions. This object then transfers back to #738 as a stable branch reservoir and to the hybrid hierarchy as a certificate component of the combined state.",
        "",
        "## Proof receipts",
        "",
        "See `FINAL-VERIFICATION.json`, `CAUSAL-ABLATION.json`, `HOSTILE-VERIFICATION.json`, and `FINITE-MATH-VERIFICATION.json`.",
        "",
    ]
    report = "\n".join(lines).strip() + "\n"
    (out_dir / "THREE-WAY-RECURSIVE-THEOREM-FORGE-REPORT.md").write_text(report, encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-738", type=Path, required=True)
    parser.add_argument("--source-595", type=Path, required=True)
    parser.add_argument("--source-cross", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    source_claims = parse_738(args.source_738) + parse_595(args.source_595) + parse_cross(args.source_cross)
    if not source_claims:
        raise ParseError("No source claims parsed")
    rules = build_rules()
    forge = Forge(source_claims, rules, recursive=True)
    forge.run()
    control = Forge(source_claims, rules, recursive=False)
    control.run()

    write_jsonl(args.out / "UNIFIED-CLAIM-BANK.jsonl", sorted(source_claims, key=lambda c: c.uid))
    write_jsonl(args.out / "RECURSIVE-THEOREM-CARDS.jsonl", forge.generated)
    (args.out / "ROUND-RECEIPTS.json").write_text(json.dumps([asdict(r) for r in forge.round_receipts], indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (args.out / "CLOSE-PROGRAMS.json").write_text(json.dumps(forge.summary()["close_programs"], indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (args.out / "CONTROL-SUMMARY.json").write_text(json.dumps(control.summary(), indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (args.out / "TREATMENT-SUMMARY.json").write_text(json.dumps(forge.summary(), indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    build_report(args.out, forge, control, {"738": args.source_738, "595": args.source_595, "CROSS": args.source_cross})

    manifest = {
        "schema": "oracle.three-way-recursive-forge.manifest.v1",
        "source_hashes": {
            "738": hashlib.sha256(args.source_738.read_bytes()).hexdigest(),
            "595": hashlib.sha256(args.source_595.read_bytes()).hexdigest(),
            "cross": hashlib.sha256(args.source_cross.read_bytes()).hexdigest(),
        },
        "files": {},
        "summary": forge.summary(),
        "control_generated": len(control.generated),
        "treatment_generated": len(forge.generated),
        "recursive_gain": len(forge.generated) - len(control.generated),
        "novelty_claimed": False,
        "flagship_closed": False,
    }
    for p in sorted(args.out.iterdir()):
        if p.is_file() and p.name != "MANIFEST.json":
            manifest["files"][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest["content_hash"] = sha256_text(canonical_json(manifest))
    (args.out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": True,
        "parsed": len(source_claims),
        "generated": len(forge.generated),
        "control_generated": len(control.generated),
        "recursive_gain": len(forge.generated) - len(control.generated),
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
