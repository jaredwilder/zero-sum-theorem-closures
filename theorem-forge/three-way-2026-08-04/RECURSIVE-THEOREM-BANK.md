# Three-Way Recursive Theorem Bank

**Date:** 2026-08-04  
**Novelty:** UNRUN  
**Lean:** UNRUN  
**Flagship closure:** NONE — exact remaining obligations are retained in `CLOSE-PROGRAMS.json`.

**Inventory:** 32 recursive theorem/target cards.

## R:R1-ESCAPEDESC — Critical Escape with Lower-Layer Ambient Defects

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-CRITICAL-ESCAPE-DESCENT`
- **Dependencies:** `738:N13, X:XLAYER04`
- **Tags:** `critical, escape, layer, recursive, triangle_cover`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `92/100`
- **Claim hash:** `586ac1b11af9081fe681b7a2f024cc878ba817b5e8aded9be1be540775b2dd87`

**Statement.** Let H_j be a finite k-critical triangle-free layer in an m-layer cover of G. For every connected S with 2 <= |S| < k, H_j has a component C outside N_{H_j}[S] with chi(C) >= k-|S|, and every ambient edge of G[C] absent from H_j[C] is covered by the other m-1 layers.

**Proof route.** Use N13 inside H_j; the final assertion is immediate from the edge cover.

**Falsifier.** Failure of the critical escape component or an ambient defect unique to H_j.

**Lean mission.** `criticalEscape_with_lowerLayerDefects`

**Novelty query.** `"critical escape component" ambient defect layers`

## R:R1-K4FIBER — K4-Free Ambient Signature-Fiber Collapse

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-K4-SIGNATURE-FIBER`
- **Dependencies:** `738:P07, X:XLINK05`
- **Tags:** `contact_signature, k4_free, recursive, triangle_free`
- **Back-transfer:** `738, 595, HYBRID`
- **Structural leverage:** `98/100`
- **Claim hash:** `f15887d1d60213b3d992c1f026dc2cfc0583ca1fd355c0f1d74772546a6bc3db`

**Statement.** Let G be K4-free, let H be any spanning subgraph, and let P be a path in H. If F is a nonempty H-contact-signature fiber on P, then G[F] is triangle-free.

**Proof route.** Choose p in the nonempty signature. Every vertex of F is adjacent to p in G, so F lies in N_G(p); XLINK05 makes that neighborhood triangle-free.

**Falsifier.** A triangle inside a nonempty signature fiber of a K4-free graph.

**Lean mission.** `K4free_signatureFiber_triangleFree`

**Novelty query.** `"K4-free" contact signature fiber triangle-free`

## R:R1-LINKRESERVE — Protected Deletion Reserve Inside Every #595 Witness Link

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-LINK-PROTECTED-RESERVE`
- **Dependencies:** `X:XLINK06, 738:N07`
- **Tags:** `chromatic, forward_link, k4_free, protected_deletion, recursive`
- **Back-transfer:** `595, 738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `be3b7b040416809a3f207c299aa48c08880c4bd756875732b4b6b5c1a9249ee5`

**Statement.** Let G be a K4-free graph with tc(G)>aleph_0 and fix any well-order. In the uncountably chromatic triangle-free forward link supplied by XLINK06, every finite sequence of protected deletions from N07 leaves an uncountably chromatic residual.

**Proof route.** XLINK06 supplies a triangle-free link of uncountable chromatic number. N07 subtracts only a finite chromatic budget, which cannot make an uncountable cardinal finite or countable.

**Falsifier.** A finite protected deletion sequence reducing the link to countable chromatic number.

**Lean mission.** `witnessLink_protectedDeletion_preserves_uncountableChromatic`

**Novelty query.** `"Erdos 595 witness" protected deletion forward neighborhood`

## R:R1-MAXCONTACT — Maximal-Layer Contact Defects Lie in the Minimal Transversal

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-MAXIMAL-CONTACT-ABSORPTION`
- **Dependencies:** `738:P07, X:XTRANS03`
- **Tags:** `contact_signature, maximal_layer, recursive, transversal`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `96/100`
- **Claim hash:** `de91ea54537fac513c937d196791bc5f99a923eebb56ce7420b06a1216a6ee9b`

**Statement.** Let H be a maximal spanning triangle-free subgraph of G and D=E(G)\E(H). For an induced path P in H, every edge internal to a fixed nonempty H-contact-signature fiber belongs to the inclusion-minimal triangle transversal D.

**Proof route.** P07 makes the fiber stable in H. XTRANS03 identifies the complement of H as a minimal transversal.

**Falsifier.** A fiber edge in H or outside both H and D.

**Lean mission.** `maximalLayer_contactDefects_in_minimalTransversal`

**Novelty query.** `"maximal triangle-free" contact signature minimal transversal`

## R:R1-SIBDEF — Sibling Defect Graphs Are Triangle-Free in K4-Free Hosts

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-SIBLING-DEFECT`
- **Dependencies:** `738:T10, X:XLINK05`
- **Tags:** `k4_free, recursive, tree, triangle_free, type_tensor`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `91/100`
- **Claim hash:** `162e897e0da5276b88e743e59b7e85401016ce92e517fdd344fc7e7de0f40b2c`

**Statement.** Let a rooted tree copy lie in a K4-free ambient graph. For every tree vertex u, the ambient graph induced by the selected children of u is triangle-free; in particular every sibling-defect graph is triangle-free, regardless of the type-tensor profile.

**Proof route.** All selected children lie in the ambient neighborhood of u, which is triangle-free by XLINK05.

**Falsifier.** Three selected children of one parent forming an ambient triangle.

**Lean mission.** `K4free_siblingDefect_triangleFree`

**Novelty query.** `"sibling defect graph" K4-free rooted tree`

## R:R1-SIGDESC — Layered Signature-Fiber Defect Descent

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-SIGNATURE-DESCENT`
- **Dependencies:** `738:P07, X:XLAYER04`
- **Tags:** `contact_signature, layer, recursive, tree, triangle_cover`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `97/100`
- **Claim hash:** `a0e7523ba9cc5f2246ca78174dfa6c03f733382207ff50b4f87718624469837a`

**Statement.** Let G be covered by m triangle-free layers H_i. Let P be an induced path in H_j and let F be the vertices outside P having one fixed nonempty H_j-contact signature on P. Then every ambient edge of G[F] is covered by the other m-1 layers, so tc(G[F]) <= m-1.

**Proof route.** P07 makes F stable in H_j. Thus H_j contributes no edge of G[F]; every ambient edge is supplied by another covering layer.

**Falsifier.** A same-signature fiber containing an edge unique to the path layer.

**Lean mission.** `layered_signatureFiber_defectDescent`

**Novelty query.** `"signature fiber" triangle-free layers defect descent`

## R:R1-SPIDERDESC — Layer-Induced Spider Defect Descent

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-SPIDER-DESCENT`
- **Dependencies:** `738:M06, X:XLAYER04`
- **Tags:** `layer, mixing, recursive, tree, triangle_cover`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `88/100`
- **Claim hash:** `1bfad87bc90baa68db0c6ff7dad8f56c02d29030996770c419251a2eaaf2c504`

**Statement.** If a spider is induced inside one layer of an m-layer triangle-free edge cover, then all ambient chords on the spider vertices are covered by the other m-1 layers.

**Proof route.** A spider is a tree. Apply layer-defect descent to the induced tree in the selected layer.

**Falsifier.** An ambient chord present only in the layer where the spider is induced.

**Lean mission.** `layerInduced_spider_defectDescent`

**Novelty query.** `"induced spider" ambient defects triangle-free layers`

## R:R1-TRANSIG — Transversal Absorption of Signature-Fiber Edges

- **Status:** `PROVED_IN_PACKET`
- **Round:** `1`
- **Rule:** `R1-TRANSVERSAL-SIGNATURE`
- **Dependencies:** `738:P07, 595:T05`
- **Tags:** `contact_signature, recursive, transversal, tree`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `95/100`
- **Claim hash:** `b675e494f567103f5e6063e26cd99e4290692b424063e06bdbd6ac2d023480f8`

**Statement.** Let D be a triangle transversal of G, put H=G-D, and let P be an induced path in the triangle-free graph H. For every fixed nonempty H-contact signature S on P, every ambient edge joining two vertices in the S-fiber belongs to D.

**Proof route.** The S-fiber is stable in H by P07, so any ambient edge internal to it was deleted and lies in D.

**Falsifier.** An internal fiber edge surviving in H.

**Lean mission.** `transversal_absorbs_signatureFiber_edges`

**Novelty query.** `"triangle transversal" contact signature fiber edges`

## R:R2-CRITABSORB — Critical Escape Defects as Lower-Layer Transversal Data

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-CRITICAL-ABSORPTION`
- **Dependencies:** `R:R1-ESCAPEDESC, 595:T05`
- **Tags:** `critical, escape, layer, recursive, transversal`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `89/100`
- **Claim hash:** `2ff5bdb1baecbeb12a3257bbb659a94a9f65e69f96d6018e4423577772ac28f9`

**Statement.** In an m-layer graph, a high-chromatic critical escape component extracted inside one triangle-free layer has all ambient nonlayer edges covered by the remaining m-1 layers; equivalently those lower layers form a triangle-free cover of the escape defect graph.

**Proof route.** This is the edge-cover conclusion of R1-ESCAPEDESC, restated in triangle-cover language.

**Falsifier.** An escape defect edge absent from every lower layer.

**Lean mission.** `criticalEscape_defectGraph_lowerLayerCover`

**Novelty query.** `"critical escape" defect graph lower layers`

## R:R2-CONTACTRED — Finite Contact-Language Reduction for Layered Defects

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-LAYERED-CONTACT-REDUCTION`
- **Dependencies:** `R:R1-SIGDESC, 738:P05`
- **Tags:** `contact_signature, fibonacci, layer, recursive, triangle_cover`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `93/100`
- **Claim hash:** `c072c48bed2cbb5b8e220b6e76bafa3d3db285fa8ec637d6a45e7c1dc403e532`

**Statement.** For an n-vertex induced path in one triangle-free layer of an m-layer graph, its vertices outside the path split into at most F_{n+2}-1 nonempty contact-signature fibers, and each fiber's ambient internal defect graph has triangle-cover number at most m-1.

**Proof route.** P05 bounds the nonempty signatures and R1-SIGDESC handles each fiber.

**Falsifier.** More than F_{n+2}-1 signatures or a fiber defect requiring m layers.

**Lean mission.** `layeredPath_contactLanguage_defectReduction`

**Novelty query.** `"Fibonacci contact signatures" layered defect graph`

## R:R2-ROOTSPLIT — Root-Level versus Deep Spider-Defect Split

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-ROOT-DEFECT-SPLIT`
- **Dependencies:** `R:R1-SPIDERDESC, R:R1-SIBDEF`
- **Tags:** `k4_free, layer, mixing, recursive, tree, triangle_cover`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `94/100`
- **Claim hash:** `f8cae9d87d642246e05c0c4bfe1b001be4c1aeb04aebbf6238562353a97b9474`

**Statement.** For a spider induced in one layer of a K4-free m-layer graph, ambient chords among first arm vertices form a triangle-free graph, while every remaining ambient chord is covered by the other m-1 layers.

**Proof route.** First arm vertices are siblings at the center, so R1-SIBDEF applies. All chords are absent from the inducing layer, so R1-SPIDERDESC covers the rest.

**Falsifier.** A root-level chord triangle or a deep chord unique to the inducing layer.

**Lean mission.** `layerSpider_rootDeep_defectSplit`

**Novelty query.** `"spider defects" root level K4-free layers`

## R:R2-SIGCOVEROBS — Countable Signature-Fiber Cover Obstruction

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-SIGNATURE-COVER-OBSTRUCTION`
- **Dependencies:** `R:R1-K4FIBER, 595:T05`
- **Tags:** `contact_signature, dispersion, k4_free, recursive, triangle_cover`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `662efb154bda92305b6e54927c507d775f3efdf745616b97b1b68fd183451ec9`

**Statement.** If G is K4-free and tc(G)>aleph_0, then no countable family of nonempty contact-signature fibers (taken from arbitrary spanning scaffolds and finite paths) has internal edge sets covering E(G).

**Proof route.** Each internal fiber graph is triangle-free by R1-K4FIBER. A countable edge cover by them would contradict tc(G)>aleph_0.

**Falsifier.** A #595 witness whose edges are covered by countably many signature fibers.

**Lean mission.** `witness_no_countable_signatureFiber_edgeCover`

**Novelty query.** `"signature fiber cover" K4-free uncountable triangle cover`

## R:R2-STABLECERT — Stable Certification of Omitted Edges

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-STABLE-CERTIFICATE`
- **Dependencies:** `X:XTRANS03, X:XLINK05`
- **Tags:** `certificate, k4_free, maximal_layer, recursive, stable, transversal`
- **Back-transfer:** `595, 738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `e88ba6455b89b60fdf7fa7c18ed5e4288888617ac7bd48445925f5aedf58d61a`

**Statement.** Let G be K4-free, H a maximal spanning triangle-free subgraph, and D=E(G)\E(H). For every omitted edge xy in D, the set W_H(xy)=N_H(x) intersect N_H(y) is nonempty and is stable in G.

**Proof route.** Maximality of H implies that adding xy creates a triangle, so W_H(xy) is nonempty. Any edge between two common neighbors together with x,y would create a K4.

**Falsifier.** An omitted edge with no H-common neighbor, or adjacent vertices in its certificate set.

**Lean mission.** `maximalTriangleFree_omittedEdge_stableCertificate`

**Novelty query.** `"maximal triangle-free subgraph" omitted edge stable common neighbors`

## R:R2-TREESEQ — Protected Tree-Sequence Extraction in a Witness Link

- **Status:** `CONDITIONAL_ON_738_SEQUENCE`
- **Round:** `2`
- **Rule:** `R2-TRANSVERSAL-TREE-SEQUENCE`
- **Dependencies:** `R:R1-LINKRESERVE, X:XCONE06`
- **Tags:** `conditional, cone, forward_link, protected_deletion, recursive, tree`
- **Back-transfer:** `738, 595, HYBRID`
- **Structural leverage:** `96/100`
- **Claim hash:** `95efb598ab958a6f357ef2941a235536a902ffe875baf1251e5df8389d648093`

**Statement.** Conditional on the #738 statements for a prescribed sequence of finite trees T_0,T_1,..., every #595 witness contains under one apex pairwise anticomplete induced copies of all T_i inside one forward link; every ambient chord within or between these copies lies outside the link layer.

**Proof route.** Use R1-LINKRESERVE to retain uncountable chromatic number after each protected deletion and apply the relevant #738(T_i) bound at every stage. Chords are absent from the induced link copies and from link-anticompleteness.

**Falsifier.** A verified #738 sequence and a witness where the recursive extraction fails.

**Lean mission.** `witnessLink_extract_treeSequence`

**Novelty query.** `"Erdos 595" pairwise anticomplete induced tree sequence link`

## R:R2-SIGCERT — Signature Defects Carry Stable Triangle Certificates

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-CERTIFIED-SIGNATURE-DEFECT`
- **Dependencies:** `R:R1-MAXCONTACT, R:R2-STABLECERT`
- **Tags:** `certificate, contact_signature, maximal_layer, recursive, transversal`
- **Back-transfer:** `595, 738, HYBRID`
- **Structural leverage:** `98/100`
- **Claim hash:** `d4bdc006fbd16df2fb9409dd4f0895c05c11d473cf0706cf3f1a67cc6ad6ea22`

**Statement.** Under R1-MAXCONTACT in a K4-free graph, every defect edge xy inside a nonempty path-signature fiber belongs to the minimal transversal and has a nonempty stable certificate set W_H(xy). Every path contact p in the shared signature is itself a certificate witness.

**Proof route.** R1-MAXCONTACT places xy in D. Since x and y both contact every p in the signature inside H, each such p lies in W_H(xy); stability follows from R2-STABLECERT.

**Falsifier.** A defect edge lacking a shared contact or with a nonstable certificate set.

**Lean mission.** `signatureDefect_has_stableCertificates`

**Novelty query.** `"contact signature defect" stable triangle certificate`

## R:R2-BOOKSTERILE — Single Stable Triangle Book Is Two-Layer Sterile

- **Status:** `PROVED_IN_PACKET`
- **Round:** `2`
- **Rule:** `R2-SINGLE-BOOK`
- **Dependencies:** `R:R2-STABLECERT, X:XCONE08`
- **Tags:** `certificate, recursive, stable, sterility, triangle_cover`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `92/100`
- **Claim hash:** `e0725721fd75615109a2cdc53551ee79d18d6d67f1a9c1391b98427381b24558`

**Statement.** Let xy be an edge and W a stable set of common neighbors of x and y. The graph on {x,y} union W has triangle-cover number exactly 2 when W is nonempty.

**Proof route.** One layer is the star from x to {y} union W; the other is the star from y to W. A triangle xyw gives the lower bound two.

**Falsifier.** A nonempty stable triangle book coverable in one layer or requiring three.

**Lean mission.** `stableTriangleBook_triangleCover_eq_two`

**Novelty query.** `"triangle book" stable pages triangle-free cover two`

## R:R3-COMMONBOOK — Common Omitted-Edge Stable Book Theorem

- **Status:** `PROVED_IN_PACKET`
- **Round:** `3`
- **Rule:** `R3-COMMON-OMITTED-BOOK`
- **Dependencies:** `R:R2-STABLECERT, X:XTRANS05`
- **Tags:** `certificate, countable_centered, k4_free, maximal_layer, recursive, transversal`
- **Back-transfer:** `595, 738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `c696860c1cbe21d66e16bfc380d0d308bf471f0e9ce250c108588b7ca283b658`

**Statement.** Let G be K4-free with tc(G)>aleph_0. For every countable family H_n of maximal spanning triangle-free subgraphs, there is an edge xy omitted from every H_n. For each n, H_n supplies a nonempty stable certificate set W_{H_n}(xy) subseteq N_G(x) intersect N_G(y).

**Proof route.** XTRANS05 gives an edge omitted by all H_n. Apply R2-STABLECERT separately to every maximal layer; all certificates lie in the common neighborhood, which is stable in a K4-free graph.

**Falsifier.** A countable maximal-layer family with no common omitted edge or a layer lacking a stable certificate.

**Lean mission.** `witness_countableMaximalLayers_commonStableBook`

**Novelty query.** `"countable maximal triangle-free subgraphs" common omitted edge stable witnesses`

## R:R3-KAPPABOOK — Cardinal Stable-Book Centeredness

- **Status:** `PROVED_IN_PACKET`
- **Round:** `3`
- **Rule:** `R3-KAPPA-OMITTED-BOOK`
- **Dependencies:** `R:R2-STABLECERT, 595:T05`
- **Tags:** `cardinal, certificate, k4_free, maximal_layer, recursive, transversal`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `0e74406f7e7d985edf97cbb36375d4d7938e4f20f393deeac4c63af436889874`

**Statement.** If G is K4-free and tc(G)>kappa, then every family of at most kappa maximal spanning triangle-free subgraphs has a common omitted edge xy, and every member supplies a nonempty stable certificate set inside N_G(x) intersect N_G(y).

**Proof route.** Use transversal centeredness T05 for the complements and R2-STABLECERT for each layer.

**Falsifier.** A family of size at most kappa with empty common complement or an uncertified omitted edge.

**Lean mission.** `triangleCover_gt_kappa_commonStableBook`

**Novelty query.** `"cardinal" maximal triangle-free layers common omitted edge`

## R:R3-FREC — Recursive Contact-Code Program for the Finite-Layer Gyárfás Hierarchy

- **Status:** `CONDITIONAL_REDUCTION`
- **Round:** `3`
- **Rule:** `R3-LAYERED-GYARFAS-RECURRENCE`
- **Dependencies:** `R:R2-CONTACTRED, X:XLAYER05`
- **Tags:** `close_reduction, contact_signature, layer, recurrence, recursive, tree`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `fba6eefcc1e0c6084e62e8c310e5d3ec90e4fbbed102dfccef432f27f94d4b94`

**Statement.** For the conjectural hierarchy f(T,m), an induced path/tree scaffold in one layer reduces each fixed contact fiber to an (m-1)-layer defect problem and reduces the total number of fiber types to a finite contact language. Thus any proof of a uniform cross-fiber gluing lemma yields an explicit recurrence from m-1 to m.

**Proof route.** R2-CONTACTRED gives finite fibers with lower layer depth; XLAYER05 supplies the induction coordinate. Only cross-fiber edges remain unsupported.

**Falsifier.** A family where within-fiber descent holds but no finite cross-fiber gluing statement can bound the hierarchy.

**Lean mission.** `finiteLayerGyarfas_contactRecurrence_reduction`

**Novelty query.** `"finite-layer Gyárfás" contact code recurrence`

## R:R3-PROFILEBASIS — Stable-Book Profile-Basis Close Reduction

- **Status:** `CONDITIONAL_REDUCTION`
- **Round:** `3`
- **Rule:** `R3-PROFILE-BASIS-REDUCTION`
- **Dependencies:** `R:R2-SIGCERT, R:R3-COMMONBOOK`
- **Tags:** `certificate, close_reduction, contact_signature, maximal_layer, recursive`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `d03a8fe96f2a5991adabd3e06342b9bbac2b89eff7057a79db8af311c6b6c823`

**Statement.** To contradict tc(G)>aleph_0 it is sufficient to construct a countable family of maximal triangle-free layers whose omitted-edge stable certificate books realize every possible path-contact certificate profile: R3-COMMONBOOK would then produce a common omitted edge with a profile already handled by one of the layers.

**Proof route.** This is a precise close reduction: completeness of the profile basis would force the common omitted edge to be included by a corresponding layer, contradicting its common omission. The load-bearing hypothesis is profile completeness.

**Falsifier.** A certificate profile not captured by the proposed countable basis or a semantic mismatch between profile handling and edge inclusion.

**Lean mission.** `stableBook_profileBasis_reduction`

**Novelty query.** `"stable certificate book" countable profile basis triangle cover`

## R:R3-TWOLAYER — Two-Layer Cross-Fiber Purification Target

- **Status:** `UNPROVED_CHECKABLE_TARGET`
- **Round:** `3`
- **Rule:** `R3-TWO-LAYER-FIBER-TARGET`
- **Dependencies:** `R:R1-K4FIBER, R:R2-CONTACTRED`
- **Tags:** `contact_signature, k4_free, layer, recursive, search_target`
- **Back-transfer:** `738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `8a9b554e9adcabd1b6ba8c1bc6afc340a23b22b79546cf255cbe1d6a7827f56f`

**Statement.** In the m=2 hybrid hierarchy, every individual nonempty contact-signature fiber is ambiently triangle-free in a K4-free host. The sole remaining purification problem is to control edges between distinct signature fibers.

**Proof route.** Within-fiber structure is settled by R1-K4FIBER; R2-CONTACTRED leaves only cross-fiber interactions.

**Falsifier.** A two-layer counterexample whose obstruction already occurs inside one signature fiber.

**Lean mission.** `twoLayer_crossFiber_purification_target`

**Novelty query.** `"two-layer" cross signature fiber induced tree purification`

## R:R3-BOOKBRANCH — Stable Book as a Clean Branch Reservoir

- **Status:** `PROVED_IN_PACKET`
- **Round:** `3`
- **Rule:** `R3-BOOK-BRANCH-BLADE`
- **Dependencies:** `R:R3-COMMONBOOK, 738:C01`
- **Tags:** `certificate, contamination, recursive, stable, transfer_blade`
- **Back-transfer:** `738, 595, HYBRID`
- **Structural leverage:** `89/100`
- **Claim hash:** `fa41e496b7a1c651e00218d7b5e0c05fcafedc61cb6bd1f230333d6ea64a2fdb`

**Statement.** The page set of every common omitted-edge book in a K4-free graph is stable. Hence, relative to any outside finite candidate set, the #738 clean-child/large-fan dichotomy applies to any chosen neighborhood subset of that page set without internal page conflicts.

**Proof route.** R3-COMMONBOOK gives a stable page set; C01 is then applicable with that set as the branch-candidate reservoir whenever its hypotheses are instantiated.

**Falsifier.** Internal adjacency among book pages or a violation of C01 under a valid instantiation.

**Lean mission.** `stableBook_cleanBranchReservoir`

**Novelty query.** `"triangle book pages" clean child fan dichotomy`

## R:R3-BOOKCANON — Stable-Book Witness Canonization Target

- **Status:** `UNPROVED_CHECKABLE_TARGET`
- **Round:** `3`
- **Rule:** `R3-BOOK-CANONIZATION-TARGET`
- **Dependencies:** `R:R3-COMMONBOOK, 738:P05`
- **Tags:** `canonization, certificate, contact_signature, recursive, search_target`
- **Back-transfer:** `595, 738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `5cdd658513671d7c06f4698c6cc38543c0539e8723e1706e19fd38635d48a458`

**Statement.** Given the common omitted edge xy from R3-COMMONBOOK, canonize the layer-specific stable witnesses by finitely many path-contact signatures relative to a protected scaffold in the high-chromatic link. A successful countable canonization would feed R3-PROFILEBASIS.

**Proof route.** P05 supplies finite contact alphabets on each finite path; the missing step is a uniform protected scaffold and compatibility across all layers.

**Falsifier.** A finite family of layers whose witnesses evade every proposed finite signature scaffold.

**Lean mission.** `stableBook_witnessCanonization_target`

**Novelty query.** `"stable triangle book" path contact canonization`

## R:R3-BOOKDISP — Stable-Book Localization–Dispersion

- **Status:** `PROVED_IN_PACKET`
- **Round:** `3`
- **Rule:** `R3-BOOK-DISPERSION`
- **Dependencies:** `R:R3-COMMONBOOK, R:R2-BOOKSTERILE`
- **Tags:** `certificate, dispersion, maximal_layer, recursive, sterility`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `99/100`
- **Claim hash:** `188fe9536b3cdd2c0a4e688adde003ea3d7b4e9a196edf6d29fb9619f57723ef`

**Statement.** Every countable attempt to cover a #595 witness by maximal triangle-free layers exposes one common stable triangle book, but that book itself has triangle-cover number two. Hence the failure of the attempted cover cannot be localized to the certificate book alone and must involve its interactions with edges outside the book.

**Proof route.** R3-COMMONBOOK constructs the book; R2-BOOKSTERILE proves it is two-layer coverable.

**Falsifier.** A common certificate book that itself has uncountable triangle-cover number.

**Lean mission.** `commonStableBook_obstruction_migrates`

**Novelty query.** `"stable triangle book" cover obstruction migration`

## R:R4-PAGECERT — Minimal-Transversal Page Certificate Theorem

- **Status:** `PROVED_IN_PACKET`
- **Round:** `4`
- **Rule:** `R4-MINIMAL-TRANSVERSAL-PAGE`
- **Dependencies:** `R:R2-STABLECERT, X:XTRANS03`
- **Tags:** `book, certificate, recursive, stable, transversal`
- **Back-transfer:** `595, 738, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `3fe5433911e3624fe69caf39c91f55338d0a12dadf01e048cd46ce367f29452e`

**Statement.** Let D be an inclusion-minimal triangle transversal of a K4-free graph and H=G-D. For every edge xy in D there is z with xz,yz in H; all such z form a stable set. Thus each minimal-transversal edge is the spine of a nonempty stable book whose pages use exactly one transversal edge.

**Proof route.** XTRANS03 makes H maximal triangle-free. Apply R2-STABLECERT. Each triangle xyz uses xy in D and its other two edges in H.

**Falsifier.** A minimal-transversal edge without an exact one-edge page certificate or with adjacent witnesses.

**Lean mission.** `minimalTransversal_edge_has_stablePageCertificates`

**Novelty query.** `"minimal triangle transversal" stable book page certificate`

## R:R4-MULTIBOOK — Multi-Book Interaction Frontier

- **Status:** `UNPROVED_CHECKABLE_TARGET`
- **Round:** `4`
- **Rule:** `R4-MULTIBOOK-INTERACTION`
- **Dependencies:** `R:R3-BOOKDISP, R:R2-BOOKSTERILE`
- **Tags:** `book, finite_search, interaction, recursive, sterility`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `8bd4e6698def2d04e15102c96649fc2f5c7d3fbf8858b05ba0fedea45b68d5ed`

**Statement.** Since every individual stable triangle book has tc=2 and the common-book obstruction migrates outside it, the first genuine finite model for #595 must involve K4-safe interactions among at least two books. Classify the smallest interaction raising tc above 2.

**Proof route.** R3-BOOKDISP and R2-BOOKSTERILE kill all single-book mechanisms.

**Falsifier.** A single stable book with tc>2, or a proof that arbitrary disjoint book unions already suffice.

**Lean mission.** `multiBook_interaction_frontier`

**Novelty query.** `"interacting triangle books" K4-free triangle cover number`

## R:R4-DOUBLESTERILE — Single-Link and Single-Book Double Sterility

- **Status:** `CONDITIONAL_REDUCTION`
- **Round:** `4`
- **Rule:** `R4-SINGLE-LINK-AND-BOOK-STERILITY`
- **Dependencies:** `X:XCONE10, R:R2-BOOKSTERILE`
- **Tags:** `book, dispersion, forward_link, recursive, sterility`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `713798a24f51f49c54558401c782ad9de6a6185bcc7afa9d83ecaed0ed9b0637`

**Statement.** Neither arbitrary complexity inside one K4-free link nor arbitrary size of one stable triangle book can force triangle-cover number above two. Any #595 construction mechanism must therefore coordinate multiple links and multiple books simultaneously.

**Proof route.** XCONE10 kills single-link complexity and R2-BOOKSTERILE kills single-book complexity.

**Falsifier.** A theorem deriving tc>2 solely from one link or one stable book.

**Lean mission.** `singleLink_singleBook_doubleSterility`

**Novelty query.** `"single link" "single triangle book" sterility`

## R:R4-PAGEFAMILY — Countable Layer Family Produces a Shared Stable Page Space

- **Status:** `PROVED_IN_PACKET`
- **Round:** `4`
- **Rule:** `R4-COUNTABLE-PAGE-FAMILY`
- **Dependencies:** `R:R3-COMMONBOOK, R:R4-PAGECERT`
- **Tags:** `certificate, countable_centered, maximal_layer, recursive, stable`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `0523a3bc35591c6461a76e7ca06f2a8deb5b4d246ebeb0a5c9cab9f68467a38a`

**Statement.** For every countable family of maximal triangle-free layers in a #595 witness, there is one edge xy such that every layer selects a nonempty subset of the same stable page space N_G(x) intersect N_G(y) as exact triangle certificates for omitting xy.

**Proof route.** R3-COMMONBOOK supplies xy and layer-specific certificate sets; R4-PAGECERT identifies them as exact page certificates in the common stable neighborhood.

**Falsifier.** A layer whose witnesses leave the common page space or do not exactly certify xy.

**Lean mission.** `countableMaximalLayers_sharedStablePageSpace`

**Novelty query.** `"shared stable page space" maximal triangle-free layers`

## R:R4-MULTIPLIER — Layer–Signature–Certificate Multiplier

- **Status:** `CONDITIONAL_REDUCTION`
- **Round:** `4`
- **Rule:** `R4-LAYER-SIGNATURE-MULTIPLIER`
- **Dependencies:** `R:R3-FREC, R:R4-PAGECERT`
- **Tags:** `certificate, contact_signature, layer, recursive, rsi_multiplier`
- **Back-transfer:** `738, 595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `f8331e23c4b23b7a4d331401b30095dbbf7d8f9228ba4dfb32aee90da3827b2a`

**Statement.** The finite-layer tree hierarchy and the #595 maximal-layer program share one recursive state object: a finite contact signature together with a lower-layer defect cover and a stable page-certificate family. Any theorem bounding this combined object transfers simultaneously to #738 purification, #595 maximal-layer bases, and the hybrid m-layer hierarchy.

**Proof route.** R3-FREC supplies signature plus lower-layer defect state; R4-PAGECERT supplies certificate state. The transfer directions are explicit, while the required bound remains open.

**Falsifier.** A bound valid in the combined state but failing one of the three stated transfer maps.

**Lean mission.** `layerSignatureCertificate_multiplier`

**Novelty query.** `"contact signature" lower layer defects stable certificates`

## R:R4-PAGECOMPACT — Page-Profile Compactness Close Program

- **Status:** `CONDITIONAL_REDUCTION`
- **Round:** `4`
- **Rule:** `R4-PAGE-PROFILE-COMPACTNESS`
- **Dependencies:** `R:R4-PAGEFAMILY, R:R3-BOOKCANON`
- **Tags:** `canonization, certificate, close_reduction, compactness, recursive`
- **Back-transfer:** `595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `3c4ab6c1cc7ba368d82b90b4196fe042f2add4b5735cfa21a3c0374ba9d3bfa5`

**Statement.** A countable canonization theorem for subsets of the shared stable page space—strong enough to choose a maximal triangle-free layer that includes the spine edge for every realized canonical profile—would refute the existence of a #595 witness.

**Proof route.** R4-PAGEFAMILY reduces every countable layer failure to one stable page space; R3-BOOKCANON identifies the missing canonization. A profile-complete layer basis contradicts common omission.

**Falsifier.** A canonical page profile for which every corresponding maximal layer must still omit the spine edge.

**Lean mission.** `pageProfile_compactness_closeReduction`

**Novelty query.** `"stable page space" canonical profiles triangle cover compactness`

## R:R4-TRICLOSE — Three-Campaign Close Interface

- **Status:** `CONDITIONAL_REDUCTION`
- **Round:** `4`
- **Rule:** `R4-THREE-CLOSE-INTERFACE`
- **Dependencies:** `R:R4-MULTIPLIER, R:R4-PAGECOMPACT`
- **Tags:** `close_reduction, recursive, rsi_multiplier, three_way`
- **Back-transfer:** `738, 595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `abf93e318bee780922494459101f82190e06d651cc475f75f8ebcb92f028071d`

**Statement.** The three flagship close programs can be synchronized around one obligation: classify combined contact-signature, lower-layer-defect, and stable-page-certificate states well enough to (i) purify induced trees, (ii) construct a countable maximal-layer basis, or (iii) prove the finite-layer hierarchy recurrence.

**Proof route.** R4-MULTIPLIER establishes the shared state object; R4-PAGECOMPACT identifies the #595 close use. The #738 and hybrid uses are supplied by R3-FREC.

**Falsifier.** A classification sufficient for one state but semantically incapable of transfer to the other two.

**Lean mission.** `threeCampaign_closeInterface`

**Novelty query.** `"three-way" induced tree triangle cover contact certificate state`

## R:R4-CENSUS — Canonical State Census Target

- **Status:** `UNPROVED_CHECKABLE_TARGET`
- **Round:** `4`
- **Rule:** `R4-CANONICAL-STATE-CENSUS`
- **Dependencies:** `R:R4-TRICLOSE, R:R3-TWOLAYER`
- **Tags:** `certificate, contact_signature, finite_search, recursive, two_layer, type_tensor`
- **Back-transfer:** `738, 595, HYBRID`
- **Structural leverage:** `100/100`
- **Claim hash:** `40a6ef7a445dad3f127e4273c75f73d39152fc199ba3eb44acb68cb197a3df8d`

**Statement.** Enumerate finite combined states consisting of a path/tree contact signature, a layer-colored defect tensor, and a stable page-certificate incidence family; quotient by isomorphism and determine the minimal forbidden states for the two-layer case.

**Proof route.** This is the finite executable form of the shared close interface, with m=2 as the first nontrivial boundary.

**Falsifier.** A missing state schema discovered by a finite graph outside the encoding or nonisomorphic states incorrectly identified.

**Lean mission.** `canonicalCombinedState_census`

**Novelty query.** `"contact signature defect tensor certificate incidence" census`
