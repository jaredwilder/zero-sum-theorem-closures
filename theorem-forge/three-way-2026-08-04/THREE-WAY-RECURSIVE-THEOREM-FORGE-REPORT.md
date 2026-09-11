# Three-Way Recursive Theorem Forge — Build, Run, and Proof Report

**Date:** 2026-08-04  
**Targets:** Erdős #738, Erdős #595, and the 738×595 cross-campaign hierarchy  
**Novelty:** UNRUN — exact queries are emitted for the local checker  
**Lean:** UNRUN — theorem names are emitted as local missions  

## Claim boundary

This run proves deterministic ingestion, typed recursive transfer, fail-closed authority handling, repeated close-program updates, hostile refusal, finite graph checks for the mathematical kernel, and causal advantage over a nonrecursive control. It does not claim either Erdős flagship is solved or that generated statements are historically novel.

## Source estate

- **738:** `ERDOS-738-ENCIRCLEMENT-THEOREM-BANK-2026-08-04(1).md` — SHA-256 `95997a5669de4860de47431e769de00d5fb68a00e5f01b4c3bb8a38f9b5391ad`
- **595:** `ERDOS-595-ENCIRCLEMENT-THEOREM-REFINERY-2026-08-04.md` — SHA-256 `f3f32d66ffea4ae56d61b12fae5ba0043a93985469267ae16f4925f7fe016d7a`
- **CROSS:** `ERDOS-738-X-595-CROSS-THEOREM-CARDS-2026-08-04.jsonl` — SHA-256 `e89d49180b7ebcbdcfd70c472ba095d7bdc2f61e38374b43462419cc0d149705`

## Run result

- Parsed source claims: **174**
- Recursive claims emitted: **32**
- Total unified claims: **206**
- Nonrecursive control claims: **9**
- Recursive gain: **23 claims**
- Back-transfers to #738: **21**
- Back-transfers to #595: **23**
- Back-transfers to hybrid hierarchy: **32**

## Highest-leverage recursive outputs

### R:R1-LINKRESERVE — Protected Deletion Reserve Inside Every #595 Witness Link
**Status:** `PROVED_IN_PACKET`  
**Rule:** `R1-LINK-PROTECTED-RESERVE`  
**Dependencies:** `X:XLINK06, 738:N07`  
**Back-transfer:** `595, 738, HYBRID`  
**Claim hash:** `be3b7b040416809a3f207c299aa48c08880c4bd756875732b4b6b5c1a9249ee5`

**Statement.** Let G be a K4-free graph with tc(G)>aleph_0 and fix any well-order. In the uncountably chromatic triangle-free forward link supplied by XLINK06, every finite sequence of protected deletions from N07 leaves an uncountably chromatic residual.

**Proof route.** XLINK06 supplies a triangle-free link of uncountable chromatic number. N07 subtracts only a finite chromatic budget, which cannot make an uncountable cardinal finite or countable.

**Falsifier.** A finite protected deletion sequence reducing the link to countable chromatic number.

**Lean mission.** `witnessLink_protectedDeletion_preserves_uncountableChromatic`

**Novelty query.** `"Erdos 595 witness" protected deletion forward neighborhood`

### R:R2-SIGCOVEROBS — Countable Signature-Fiber Cover Obstruction
**Status:** `PROVED_IN_PACKET`  
**Rule:** `R2-SIGNATURE-COVER-OBSTRUCTION`  
**Dependencies:** `R:R1-K4FIBER, 595:T05`  
**Back-transfer:** `595, HYBRID`  
**Claim hash:** `662efb154bda92305b6e54927c507d775f3efdf745616b97b1b68fd183451ec9`

**Statement.** If G is K4-free and tc(G)>aleph_0, then no countable family of nonempty contact-signature fibers (taken from arbitrary spanning scaffolds and finite paths) has internal edge sets covering E(G).

**Proof route.** Each internal fiber graph is triangle-free by R1-K4FIBER. A countable edge cover by them would contradict tc(G)>aleph_0.

**Falsifier.** A #595 witness whose edges are covered by countably many signature fibers.

**Lean mission.** `witness_no_countable_signatureFiber_edgeCover`

**Novelty query.** `"signature fiber cover" K4-free uncountable triangle cover`

### R:R2-STABLECERT — Stable Certification of Omitted Edges
**Status:** `PROVED_IN_PACKET`  
**Rule:** `R2-STABLE-CERTIFICATE`  
**Dependencies:** `X:XTRANS03, X:XLINK05`  
**Back-transfer:** `595, 738, HYBRID`  
**Claim hash:** `e88ba6455b89b60fdf7fa7c18ed5e4288888617ac7bd48445925f5aedf58d61a`

**Statement.** Let G be K4-free, H a maximal spanning triangle-free subgraph, and D=E(G)\E(H). For every omitted edge xy in D, the set W_H(xy)=N_H(x) intersect N_H(y) is nonempty and is stable in G.

**Proof route.** Maximality of H implies that adding xy creates a triangle, so W_H(xy) is nonempty. Any edge between two common neighbors together with x,y would create a K4.

**Falsifier.** An omitted edge with no H-common neighbor, or adjacent vertices in its certificate set.

**Lean mission.** `maximalTriangleFree_omittedEdge_stableCertificate`

**Novelty query.** `"maximal triangle-free subgraph" omitted edge stable common neighbors`

### R:R3-BOOKCANON — Stable-Book Witness Canonization Target
**Status:** `UNPROVED_CHECKABLE_TARGET`  
**Rule:** `R3-BOOK-CANONIZATION-TARGET`  
**Dependencies:** `R:R3-COMMONBOOK, 738:P05`  
**Back-transfer:** `595, 738, HYBRID`  
**Claim hash:** `5cdd658513671d7c06f4698c6cc38543c0539e8723e1706e19fd38635d48a458`

**Statement.** Given the common omitted edge xy from R3-COMMONBOOK, canonize the layer-specific stable witnesses by finitely many path-contact signatures relative to a protected scaffold in the high-chromatic link. A successful countable canonization would feed R3-PROFILEBASIS.

**Proof route.** P05 supplies finite contact alphabets on each finite path; the missing step is a uniform protected scaffold and compatibility across all layers.

**Falsifier.** A finite family of layers whose witnesses evade every proposed finite signature scaffold.

**Lean mission.** `stableBook_witnessCanonization_target`

**Novelty query.** `"stable triangle book" path contact canonization`

### R:R3-COMMONBOOK — Common Omitted-Edge Stable Book Theorem
**Status:** `PROVED_IN_PACKET`  
**Rule:** `R3-COMMON-OMITTED-BOOK`  
**Dependencies:** `R:R2-STABLECERT, X:XTRANS05`  
**Back-transfer:** `595, 738, HYBRID`  
**Claim hash:** `c696860c1cbe21d66e16bfc380d0d308bf471f0e9ce250c108588b7ca283b658`

**Statement.** Let G be K4-free with tc(G)>aleph_0. For every countable family H_n of maximal spanning triangle-free subgraphs, there is an edge xy omitted from every H_n. For each n, H_n supplies a nonempty stable certificate set W_{H_n}(xy) subseteq N_G(x) intersect N_G(y).

**Proof route.** XTRANS05 gives an edge omitted by all H_n. Apply R2-STABLECERT separately to every maximal layer; all certificates lie in the common neighborhood, which is stable in a K4-free graph.

**Falsifier.** A countable maximal-layer family with no common omitted edge or a layer lacking a stable certificate.

**Lean mission.** `witness_countableMaximalLayers_commonStableBook`

**Novelty query.** `"countable maximal triangle-free subgraphs" common omitted edge stable witnesses`

### R:R3-FREC — Recursive Contact-Code Program for the Finite-Layer Gyárfás Hierarchy
**Status:** `CONDITIONAL_REDUCTION`  
**Rule:** `R3-LAYERED-GYARFAS-RECURRENCE`  
**Dependencies:** `R:R2-CONTACTRED, X:XLAYER05`  
**Back-transfer:** `738, HYBRID`  
**Claim hash:** `fba6eefcc1e0c6084e62e8c310e5d3ec90e4fbbed102dfccef432f27f94d4b94`

**Statement.** For the conjectural hierarchy f(T,m), an induced path/tree scaffold in one layer reduces each fixed contact fiber to an (m-1)-layer defect problem and reduces the total number of fiber types to a finite contact language. Thus any proof of a uniform cross-fiber gluing lemma yields an explicit recurrence from m-1 to m.

**Proof route.** R2-CONTACTRED gives finite fibers with lower layer depth; XLAYER05 supplies the induction coordinate. Only cross-fiber edges remain unsupported.

**Falsifier.** A family where within-fiber descent holds but no finite cross-fiber gluing statement can bound the hierarchy.

**Lean mission.** `finiteLayerGyarfas_contactRecurrence_reduction`

**Novelty query.** `"finite-layer Gyárfás" contact code recurrence`

### R:R3-KAPPABOOK — Cardinal Stable-Book Centeredness
**Status:** `PROVED_IN_PACKET`  
**Rule:** `R3-KAPPA-OMITTED-BOOK`  
**Dependencies:** `R:R2-STABLECERT, 595:T05`  
**Back-transfer:** `595, HYBRID`  
**Claim hash:** `0e74406f7e7d985edf97cbb36375d4d7938e4f20f393deeac4c63af436889874`

**Statement.** If G is K4-free and tc(G)>kappa, then every family of at most kappa maximal spanning triangle-free subgraphs has a common omitted edge xy, and every member supplies a nonempty stable certificate set inside N_G(x) intersect N_G(y).

**Proof route.** Use transversal centeredness T05 for the complements and R2-STABLECERT for each layer.

**Falsifier.** A family of size at most kappa with empty common complement or an uncertified omitted edge.

**Lean mission.** `triangleCover_gt_kappa_commonStableBook`

**Novelty query.** `"cardinal" maximal triangle-free layers common omitted edge`

### R:R3-PROFILEBASIS — Stable-Book Profile-Basis Close Reduction
**Status:** `CONDITIONAL_REDUCTION`  
**Rule:** `R3-PROFILE-BASIS-REDUCTION`  
**Dependencies:** `R:R2-SIGCERT, R:R3-COMMONBOOK`  
**Back-transfer:** `595, HYBRID`  
**Claim hash:** `d03a8fe96f2a5991adabd3e06342b9bbac2b89eff7057a79db8af311c6b6c823`

**Statement.** To contradict tc(G)>aleph_0 it is sufficient to construct a countable family of maximal triangle-free layers whose omitted-edge stable certificate books realize every possible path-contact certificate profile: R3-COMMONBOOK would then produce a common omitted edge with a profile already handled by one of the layers.

**Proof route.** This is a precise close reduction: completeness of the profile basis would force the common omitted edge to be included by a corresponding layer, contradicting its common omission. The load-bearing hypothesis is profile completeness.

**Falsifier.** A certificate profile not captured by the proposed countable basis or a semantic mismatch between profile handling and edge inclusion.

**Lean mission.** `stableBook_profileBasis_reduction`

**Novelty query.** `"stable certificate book" countable profile basis triangle cover`

### R:R3-TWOLAYER — Two-Layer Cross-Fiber Purification Target
**Status:** `UNPROVED_CHECKABLE_TARGET`  
**Rule:** `R3-TWO-LAYER-FIBER-TARGET`  
**Dependencies:** `R:R1-K4FIBER, R:R2-CONTACTRED`  
**Back-transfer:** `738, HYBRID`  
**Claim hash:** `8a9b554e9adcabd1b6ba8c1bc6afc340a23b22b79546cf255cbe1d6a7827f56f`

**Statement.** In the m=2 hybrid hierarchy, every individual nonempty contact-signature fiber is ambiently triangle-free in a K4-free host. The sole remaining purification problem is to control edges between distinct signature fibers.

**Proof route.** Within-fiber structure is settled by R1-K4FIBER; R2-CONTACTRED leaves only cross-fiber interactions.

**Falsifier.** A two-layer counterexample whose obstruction already occurs inside one signature fiber.

**Lean mission.** `twoLayer_crossFiber_purification_target`

**Novelty query.** `"two-layer" cross signature fiber induced tree purification`

### R:R4-CENSUS — Canonical State Census Target
**Status:** `UNPROVED_CHECKABLE_TARGET`  
**Rule:** `R4-CANONICAL-STATE-CENSUS`  
**Dependencies:** `R:R4-TRICLOSE, R:R3-TWOLAYER`  
**Back-transfer:** `738, 595, HYBRID`  
**Claim hash:** `40a6ef7a445dad3f127e4273c75f73d39152fc199ba3eb44acb68cb197a3df8d`

**Statement.** Enumerate finite combined states consisting of a path/tree contact signature, a layer-colored defect tensor, and a stable page-certificate incidence family; quotient by isomorphism and determine the minimal forbidden states for the two-layer case.

**Proof route.** This is the finite executable form of the shared close interface, with m=2 as the first nontrivial boundary.

**Falsifier.** A missing state schema discovered by a finite graph outside the encoding or nonisomorphic states incorrectly identified.

**Lean mission.** `canonicalCombinedState_census`

**Novelty query.** `"contact signature defect tensor certificate incidence" census`

### R:R4-DOUBLESTERILE — Single-Link and Single-Book Double Sterility
**Status:** `CONDITIONAL_REDUCTION`  
**Rule:** `R4-SINGLE-LINK-AND-BOOK-STERILITY`  
**Dependencies:** `X:XCONE10, R:R2-BOOKSTERILE`  
**Back-transfer:** `595, HYBRID`  
**Claim hash:** `713798a24f51f49c54558401c782ad9de6a6185bcc7afa9d83ecaed0ed9b0637`

**Statement.** Neither arbitrary complexity inside one K4-free link nor arbitrary size of one stable triangle book can force triangle-cover number above two. Any #595 construction mechanism must therefore coordinate multiple links and multiple books simultaneously.

**Proof route.** XCONE10 kills single-link complexity and R2-BOOKSTERILE kills single-book complexity.

**Falsifier.** A theorem deriving tc>2 solely from one link or one stable book.

**Lean mission.** `singleLink_singleBook_doubleSterility`

**Novelty query.** `"single link" "single triangle book" sterility`

### R:R4-MULTIBOOK — Multi-Book Interaction Frontier
**Status:** `UNPROVED_CHECKABLE_TARGET`  
**Rule:** `R4-MULTIBOOK-INTERACTION`  
**Dependencies:** `R:R3-BOOKDISP, R:R2-BOOKSTERILE`  
**Back-transfer:** `595, HYBRID`  
**Claim hash:** `8bd4e6698def2d04e15102c96649fc2f5c7d3fbf8858b05ba0fedea45b68d5ed`

**Statement.** Since every individual stable triangle book has tc=2 and the common-book obstruction migrates outside it, the first genuine finite model for #595 must involve K4-safe interactions among at least two books. Classify the smallest interaction raising tc above 2.

**Proof route.** R3-BOOKDISP and R2-BOOKSTERILE kill all single-book mechanisms.

**Falsifier.** A single stable book with tc>2, or a proof that arbitrary disjoint book unions already suffice.

**Lean mission.** `multiBook_interaction_frontier`

**Novelty query.** `"interacting triangle books" K4-free triangle cover number`

## Three simultaneous close programs

### CLOSE-738 — Erdos #738
- Resolved obligations: **1**
- Remaining exact obligations: `cross_fiber_gluing, two_layer_purification, finite_layer_recurrence, combined_state_classification`

### CLOSE-595 — Erdos #595
- Resolved obligations: **2**
- Remaining exact obligations: `page_profile_canonization, countable_maximal_layer_basis, multi_link_multi_book_interaction`

### CLOSE-HYBRID — Finite-layer induced-tree hierarchy
- Resolved obligations: **2**
- Remaining exact obligations: `cross_fiber_gluing, finite_layer_recurrence, combined_state_classification`

## Strongest new recursive seam

A maximal spanning triangle-free layer in a K4-free graph certifies each omitted edge by a nonempty stable set of common-neighbor pages. Countable transversal centeredness then forces every countable family of maximal layers in a #595 witness to omit one common edge and to choose its certificates from one shared stable page space. The page space is itself two-layer sterile, so the true obstruction lies in page-profile and inter-book interactions. This object then transfers back to #738 as a stable branch reservoir and to the hybrid hierarchy as a certificate component of the combined state.

## Proof receipts

See `FINAL-VERIFICATION.json`, `CAUSAL-ABLATION.json`, `HOSTILE-VERIFICATION.json`, and `FINITE-MATH-VERIFICATION.json`.
