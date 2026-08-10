# Adjudication Ledger

Project: tnbench — independent classical benchmarking of QAT submissions
Instance under review: `floquet_mixed_field_ising_zzd3_51qx16c`
Upstream SHA: `29bf4d07fa3a16c8d280e717780633299da84c27`
Last updated: 2026-08-10

**Rules.** No claim enters as TRUE. Assertions from Claude or GPT enter as
CLAIMED and are promoted only by executable check, independent
re-derivation, or a cited primary source. Our own refuted claims stay in
the ledger — a project auditing someone else's disclosure discipline does
not hide its own corrections.

Status values: VERIFIED · VERIFIED EXTERNALLY · PARTIAL · UNVERIFIED ·
REJECTED · FALSE · PROBABLE · NOT ESTABLISHED · CONFOUNDED

---

## Current thesis (frozen 2026-08-10)

> Given that the published magnetization SPP results remain sensitive to
> the reported truncation settings at cycle 16, what convergence evidence
> supports treating the single-setting ZZ_{d=3} SPP value at
> W=16, ε₀=5×10⁻⁸ as a quantitatively controlled classical comparator?

No claim that 0.183429 is incorrect is made or required.

---

## A. Claims about the reported results

| ID | Claim | Status | Basis |
|---|---|---|---|
| C1a | SPP lies below the QESEM interval at cycles 13, 14, 16, 26, 29, 30 and inside at 15 (6 below, 1 inside, 0 above). | VERIFIED | Direct recount of upstream values. |
| C1b | SPP lies below the QESEM central estimate at all seven reported cycles. | VERIFIED | All seven signed residuals negative. |
| C1c | The one-sided pattern proves truncation biases SPP downward. | REJECTED | Sparse-Pauli coefficients carry sign/phase; no generic monotonicity theorem relates truncation to the sign of the observable error. Descriptive only. **Excluded from public comment.** |
| C3 | PEPS-BP and SPP uniformly bracket QESEM at late times. | PARTIAL | Strict interval bracketing at cycles 14, 16, 26, 29, 30. At 15 SPP is inside; at 13 both classical values are below. Original "uniform late-time" phrasing was wrong. |
| E1 | Magnetization cycle 16: SPP settings (W=11, ε₀=1e-11) → 0.41110594 and (W=20, ε₀=1e-9) → 0.38697176, differing by 0.02413418 — 1.133× the QESEM half-width of 0.02130. | VERIFIED | Arithmetic on published values. **Load-bearing for the public thesis.** |
| E2 | Cross-observable comparison: mean per-cycle signed relative residual −5.06% for ZZd2 (ε₀=1e-9) vs −12.50% for ZZd3 (ε₀=5e-8); −6.23% for ZZd2 excluding the cycle-29 duplicate. | CONFOUNDED | Varies ε₀ and observable weight requirement simultaneously; d=3 correlators need longer Pauli strings at fixed W=16. Directionally suggestive, evidentially useless. **Excluded from public comment.** |
| T1 | The N=51 ZZd3 SPP value is demonstrated converged. | NOT ESTABLISHED | Single (W, ε₀) tabulated; live tracker reports no SPP bounds; submitters state classical convergence is not convincing. |
| T2 | The N=51 ZZd3 SPP value is demonstrated downward-biased. | NOT ESTABLISHED | See C1c. |

## B. Claims about the circuit and geometry

| ID | Claim | Status | Basis |
|---|---|---|---|
| C2a | RZZ(π/3) splits an anticommuting Pauli into two terms with coefficient magnitudes 0.5 and 0.866025. | VERIFIED | Exact Pauli conjugation algebra. |
| C2a′ | Those branches are "near-equal." | OVERSTATED | Amplitude ratio 1.73; squared weights 0.25 : 0.75. Correct statement: both branches are substantial. |
| C2b | The applied RX rotation is near π/2 / near-Clifford. | FALSE | The circuit applies RX(θx/3) = RX(0.5218893…) ≈ π/6, not RX(θx) ≈ π/2. Claude read the parameter table instead of the gate list. |
| C2c | RX(θx/3) produces substantial branching. | VERIFIED | \|cos\| = 0.866879, \|sin\| = 0.498519. |
| C2d | The parameters were chosen deliberately to defeat sparse-Pauli methods. | UNVERIFIED — SPECULATION | Non-Cliffordness is fact; intent is not. **Excluded from public comment.** |
| C4 | Any intermediate Pauli containing X or Y may be discarded exactly during backward propagation. | FALSE | Two-RX counterexample: a discarded Y component can rotate back into Z and contribute. Exact deletion is valid only at terminal projection onto \|0⟩^⊗N, or at a cut after which all remaining gates are computational-basis diagonal. |
| C5 | A 16–20-qubit replica can quantitatively establish truncation behaviour of the N=51 late-cycle calculation. | REJECTED | Two independent causal-cone derivations show that by cycle 10 all 86 ZZd3 terms have formal backward support cones spanning the 51-qubit patch. **Therefore no 16–20-qubit reduction is justified by support containment for cycle 13+.** This does *not* establish that the exact observable numerically depends on every qubit, nor that a small-patch approximation must be inaccurate. |
| F1 | ZZd3 contains 84 graph-distance-3 pairs. | FALSE | Graph reconstruction from the upstream edge layers gives 86 unordered distance-3 pairs; the README list has 86 unique entries matching that set exactly. N_d3 = 86. A reproducer normalising by 84 computes a different observable (2.4% shift, comparable to several residuals under discussion). |
| F2 | `verify_env.py` PEPS memory model assumed 17 degree-3 and 34 degree-2 sites. | FALSE | Degree histogram from the reconstructed graph is {2: 41, 3: 10}. All printed memory figures were ~1.67× too large. Corrected in f4a8112. |

## C. Method claims

| ID | Claim | Status | Basis |
|---|---|---|---|
| N1 | SPP admits no useful a priori error bound, because the 1-norm governing expectation-value error can grow by up to √2 per branching gate while only the 2-norm is conserved. | CLAIMED — CLAUDE'S REASONING | Explains why a naive coefficient-wise bound is useless. Does **not** prove that no tighter method-specific certificate can exist. Not needed for the thesis; retained as a technical note. |
| N2 | The ORQA methodology treats truncation accuracy as strongly system-dependent, with systematic ε₀ convergence checks identified as important. | VERIFIED EXTERNALLY | Authors' own published methodology. Preferred over N1 for public use. |
| N3 | The QAT observable-estimation pathway describes rigorous error bars as part of validation, while this classical comparator reports none. | EVIDENTIARY TENSION — NOT A RULES VIOLATION | Other tracker entries also carry N/A bounds. Phrase as a question, never as a schema violation. |

## D. External verifications

| ID | Claim | Status | Basis |
|---|---|---|---|
| V1 | Live QAT assigns an uncertainty interval to the SPP/ORQA value 0.183429. | FALSE | Live tracker reports `0.183429 [N/A, N/A]`, W=16, ε₀=5e-8, 7,960 s, 12,288 Fugaku nodes. |
| V2 | ORQA paper arXiv:2506.13241 accepted in Physical Review Applied. | VERIFIED EXTERNALLY | Accepted 2026-07-14, DOI 10.1103/y8ft-m61w. Describe as *accepted*, not as version of record. |

## E. Anomalies in the source

| ID | Claim | Status | Basis |
|---|---|---|---|
| A1 | ZIZ cycle-29 SPP value is 0.250253, identical to cycle 16 to six decimals. | VERIFIED ANOMALY | Cycle 16: 0.250253 / 31,559 s. Cycle 29: 0.250253 / 42,506 s. Introduced by PR #230 alongside other late-cycle rows; the cycle-16 row pre-existed. Cycle-29 value also breaks local trend (0.2355 at 26, 0.23 at 30). |
| A2 | The duplicate is definitely a transcription error. | PROBABLE — NOT PROVEN | Differing runtimes are consistent with a genuine rerun. Confirmation requires the underlying result artifact or submitter clarification. Ask; do not assert. |

## F. Our own refuted work

| ID | Claim | Status | Basis |
|---|---|---|---|
| A3 | GPT's initial causal-cone table gave cycles 5/6/7/8 as min 32, 39, 45, 50 with full-51 counts 21, 42, 68, 80. | REFUTED | The derivation permitted support expansion before the terminal ZZ observable had crossed the first backward RX layer. Setting `transverse=True` at initialisation reproduces those numbers exactly, confirming the mechanism. Corrected verifier and Claude's independent reimplementation both give min 28/32/39/45/50/51/51 and full-51 counts 11/32/62/75/85/86/86 for cycles 5–10, 13. |
| A4 | Claude's reported cross-observable mean residuals of −5.29% (ZZd2) and −12.66% (ZZd3). | REFUTED | Computed with an invalid aggregation formula. Correct per-cycle means are −5.06% and −12.50%; −6.23% for ZZd2 excluding cycle 29. Superseded by E2, which is itself excluded as confounded. |
| A5 | Claude's proposal to "submit the QuantaCore↔Eigenspectrum platform to the QAT." | REJECTED | No such pathway exists. QAT accepts problem instances and results across three pathways; there is no platform or methodology submission route. |

---

## Verifier invariants

The committed verifier must continue to reproduce, from the frozen
upstream edge lists:

- 56 unique edges (19 / 19 / 18 across E1 / E2 / E3)
- degree histogram {2: 41, 3: 10}
- graph connected, 51/51 reachable
- 71 distance-2 pairs, 86 distance-3 pairs
- README d=3 pair set equal to the graph-derived set
- cone table: min 28/32/39/45/50/51/51 and full-51 counts
  11/32/62/75/85/86/86 at cycles 5, 6, 7, 8, 9, 10, 13

Assumptions that must be executable assertions, not comments:
`sin(θx/3) ≠ 0` and `sin(θzz) ≠ 0`. A θz assertion is not required —
RZ rotates transverse content within the transverse plane and is not
what creates support-expansion capability.
