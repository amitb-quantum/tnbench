# tnbench — Project Brief v1

**Date:** 2026-08-10
**Repo:** `~/tnbench` (private)
**Upstream instance SHA:** see `instances/UPSTREAM_SHA`

---

## 1. Goal

Earn standing in the Quantum Advantage Tracker (QAT) community as an
independent adjudicator of classical-vs-quantum claims, and — if the
evidence supports it — produce a submission.

**Non-goal:** producing a quantum advantage claim of our own. We have a
156-qubit IBM Heron (Kingston) with ~156 QPU-minutes remaining. That is
not competitive against Qedma/Algorithmiq-scale efforts and the heavy-hex
degree-3 topology is structurally disadvantaged for hardness claims.

**Route in.** QAT accepts three pathways (observable estimations,
variational problems, classically verifiable problems) and three
categories (Active, Superseded, Baseline). Issue #153 demonstrates the
cheap door: a purely classical result, produced on a laptop CPU, that
demotes a quantum claim. No QPU required. Public review comments on open
submissions require no submission at all.

**Immediate question.** Is the SPP (ORQA) entry for
`floquet_mixed_field_ising_zzd3_51qx16c` converged, or is it a
truncation-biased estimate presented without a convergence study?

---

## 2. Established facts

All independently verifiable from the upstream repo or the terminal.
Nothing in this section is inference.

### 2.1 The instance

- 51 qubits, IBM heavy-hex connectivity, indices 0–50.
- Initial state |0⟩^⊗51.
- 16 Floquet cycles. U_F = U_3 · U_2 · U_1.
- Each layer: `U_m = ∏_{(j,k)∈E_m} RZZ(θzz) ∏_i RZ(θz/3) ∏_i RX(θx/3)`
- Edge partition: |E_1| = 19, |E_2| = 19, |E_3| = 18. Total 56 edges.
- Parameters: θx = 1.56567, θz = 0.33879, θzz = π/3.
- QASM confirms: `rx(0.5218893140942666)` = θx/3,
  `rz(0.11293116821573333)` = θz/3, `rzz(pi/3)`.
- `rzz` is macro-defined in the QASM as cx · rz(p0) · cx.

### 2.2 Gate census (`..._zzd3_51qx16c.qasm`)

| gate | count | check |
|---|---|---|
| rx | 2448 | 51 × 48 layers ✓ |
| rz | 2448 | 51 × 48 layers ✓ |
| rzz | 896 | 56 edges × 16 cycles ✓ |
| barrier | 48 | one per layer ✓ |

No measurement instructions. Observable applied in post-processing.

### 2.3 Observable

`ZZ_d3 = (1/N_d3) Σ_{(i,j): d(i,j)=3} Z_i Z_j`, averaged over the
86-pair list given in the upstream README.

### 2.4 Reported results, zzd3, N=51

| Cycle | QESEM (lo, hi) | PEPS-BP BD=700 | SPP W=16 ε₀=5e-8 | SPP runtime |
|---|---|---|---|---|
| 13 | 0.2278 (0.2183, 0.2374) | 0.21647733 | 0.1885839 | 7,061 s |
| 14 | 0.2020 (0.1935, 0.2106) | 0.21814969 | 0.19071564 | 7,405 s |
| 15 | 0.1909 (0.1822, 0.1997) | 0.22427787 | 0.1884349 | 7,699 s |
| 16 | 0.2111 (0.1984, 0.2238) | 0.2519062 | 0.18342936 | 7,961 s |
| 26 | 0.2041 (0.2009, 0.2074) | 0.352624 | 0.1679 | 10,093 s |
| 29 | 0.1920 (0.1893, 0.1947) | 0.341418 | 0.1643 | 10,629 s |
| 30 | 0.1993 (0.1948, 0.2039) | 0.356932 | 0.163156 | 10,800 s |

Cycles 26/29/30 use QESEM (ZNE); 13–16 use QESEM (unbiased).

### 2.5 Truncation settings across observables

| Observable | SPP settings reported | cheapest runtime |
|---|---|---|
| Magnetization | (W=11, ε₀=1e-11) and (W=20, ε₀=1e-9) | 22,228 s |
| ZIZ (d=2) | (W=16, ε₀=1e-9) | 27,435 s |
| ZIIZ (d=3) | (W=16, ε₀=5e-8) — single setting | 7,061 s |

### 2.6 Compute asymmetry

- SPP: 12,288 Fugaku nodes, 65,536 cores. Peak tracked paths ~10¹²
  (stated for magnetization).
- PEPS-BP: 128 vCPU (AMD EPYC 7R13), 334 GiB RAM.
- Ours: 20-core Intel Ultra 285K (24 threads), 20 GiB WSL RAM,
  RTX 5090 32 GiB.
- Measured: GPU complex64 87,902 GFLOP/s; GPU complex128 1,652 GFLOP/s
  (53.2× penalty); CPU complex128 925 GFLOP/s. GPU c64 : CPU c128 ≈ 95×.
- complex64 vs complex128 agreement: 2.0e-7 relative. Single precision
  is safe.

### 2.7 What the submitters themselves state

The upstream README says neither classical method achieves convincing
convergence; PEPS-BP is reliable only to N_c ≈ 12; SPP runs disagree
with each other and with the quantum data beyond 7 cycles. For
magnetization, the (11, 1e-11) and (20, 1e-9) runs consume comparable
resources and still diverge, and both are phase-shifted relative to the
quantum data.

**This is disclosed, not hidden.** Any critique must engage with the
disclosure rather than present non-convergence as a discovery.

---

## 3. Contested claims — asserted by Claude, NOT verified

Each needs independent derivation or an executable check. Do not treat
any as established.

**C1 — SPP zzd3 is one-sided low.**
Claim: SPP falls below the QESEM interval at cycles 13, 14, 16, 26, 29,
30 and inside it at 15 — six of seven below, never above. Claimed
significance: truncation discards weight, biasing magnitude downward, so
one-sidedness is the signature of an unconverged estimate rather than a
converged disagreement.
*Status: counts done by eye from the table in §2.4. Recount required.
Whether one-sidedness is statistically meaningful at n=7 is unaddressed.*

**C2 — the parameters are deliberately anti-SPP.**
Claim: θzz = π/3 gives conjugation weights cos = 0.5, sin = 0.866, so
anticommuting Paulis split into near-equal branches; θx = 1.56567 is
0.0051 rad below π/2, near-Clifford but detuned. Contrast with Kim et al.
2023 where θzz = π/2 was Clifford, which enabled the classical refutations.
*Status: the arithmetic is checkable. The claim about intent is
speculation and should be dropped from any public comment.*

**C3 — PEPS-BP and SPP bracket the quantum result.**
Claim, already partially retracted: PEPS-BP is above the QESEM interval
at 14, 15, 16, 26, 29, 30 but **below** it at cycle 13 (0.2165 vs lower
bound 0.2183). Bracketing is therefore a late-time phenomenon, not
uniform.
*Status: needs recount. Earlier phrasing said "bracket from opposite
sides" without the cycle-13 exception and was wrong.*

**C4 — X/Y pruning is valid and is the largest constant-factor win.**
Claim: since the initial state is |0⟩^⊗51, any propagated Pauli string
containing an X or Y factor has zero expectation and can be discarded at
every layer.
*Status: the zero-expectation part is standard. Whether pruning at
**every** layer (rather than only at the end) is correct under backward
Heisenberg propagation needs derivation — it may discard paths that
recombine. This is the most likely place for a silent bug.*

**C5 — a 16–20 qubit replica yields evidence about the 51-qubit claim.**
Claim: build the same Floquet circuit on a small heavy-hex patch, solve
exactly by statevector, sweep ε₀ at W=16, and use the signed-error-vs-ε₀
curve to argue about the 51-qubit SPP point.
*Status: **this is the load-bearing assumption of the whole plan and it
is weak.** Extrapolating truncation behaviour across system size is
precisely the move we would criticise in someone else's submission. SPP
cost and error both depend on path count, which grows with system size
and depth in ways a 16-qubit system may not represent. If C5 fails, the
plan needs replacing, not patching.*

---

## 4. Method discipline

- Every load-bearing claim gets an executable check or is marked
  UNVERIFIED in `notes/`.
- Predictions are written and committed **before** the run that tests
  them.
- Runs freeze a config, hash it, log the hash with the result.
- Upstream artifacts referenced by SHA, never vendored.
- Claude's assertions enter the ledger as CLAIMED, never as TRUE.

---

## 5. Questions for independent derivation

Answer without reference to §3 where possible.

1. Under backward Heisenberg propagation of Z_i Z_j through this circuit,
   at which points may a Pauli string containing X or Y be discarded
   without changing the final expectation value against |0⟩^⊗51?
2. What is the branching factor per RZZ(π/3) for an anticommuting Pauli,
   and what does that imply for path count growth over 16 cycles?
3. Does the RX(θx/3) angle being near π/2 help or hurt a sparse-Pauli
   method, and why?
4. Recount C1 and C3 directly from §2.4. Report disagreements.
5. Is there any defensible way to reason from a small-N SPP convergence
   study to the N=51 result? If not, what would a valid critique of the
   zzd3 entry require instead?
