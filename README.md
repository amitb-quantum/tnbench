# tnbench

**Provenance-first independent adjudication of classical comparators in quantum-advantage claims.**

`tnbench` is a small, evidence-disciplined project for independently checking the *classical* side of public quantum-advantage submissions. The initial case study examines Sparse Pauli Propagation (SPP/ORQA) results for the Quantum Advantage Tracker (QAT) Floquet mixed-field Ising benchmark.

The project is not attempting to make a quantum-advantage claim of its own, and it does **not** claim that the reported SPP value is wrong. Its purpose is narrower: reconstruct the published instance, verify load-bearing facts from frozen upstream artifacts, record corrections openly, and ask what convergence evidence supports treating a single classical estimate as quantitatively controlled.

> **Current adjudication question**
>
> Given that the published magnetization SPP results remain sensitive to the reported truncation settings at cycle 16, what convergence evidence supports treating the single-setting `ZZ_{d=3}` SPP value at `W=16, ε₀=5×10⁻⁸` as a quantitatively controlled classical comparator?

## Status

**Adjudication snapshot:** [`v0.1.0-adjudication`](https://github.com/amitb-quantum/tnbench/releases/tag/v0.1.0-adjudication)

**Primary QAT instance under review:**

- `floquet_mixed_field_ising_zzd3_51qx16c`
- SPP / ORQA
- `W = 16`
- `ε₀ = 5×10⁻⁸`
- reported observable value: `0.183429`
- QAT submission: [issue #171](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/171)

The frozen adjudication snapshot contains the geometry reconstruction, causal-cone verifier, machine-readable output, adjudication ledger, and draft review comments. Documentation on `main` may continue to improve, but the tag records the pre-public-comment technical state.

---

## Why this project exists

Quantum-advantage claims are comparative claims. A quantum result is only as meaningful as the classical comparator used against it, and in hard many-body benchmarks the classical side is often approximate, truncated, or resource-limited.

That creates a useful role for independent adjudication even without matching the original supercomputer budget:

1. reconstruct the exact problem instance from public artifacts;
2. verify topology, observables, gate ordering, and normalizations rather than infer them from prose;
3. distinguish reported facts from interpretation;
4. identify what is and is not demonstrated by the published convergence evidence;
5. preserve corrections to our own analysis rather than silently rewriting history.

The emphasis is therefore **verification before simulation**. A new large computation is not automatically more informative than a careful audit of what the existing result actually establishes.

---

## Case study: 51-qubit Floquet mixed-field Ising

The current target is a 51-qubit IBM heavy-hex patch evolved under a mixed-field Floquet Ising circuit. The upstream circuit uses three disjoint RZZ edge layers per Floquet cycle and reports magnetization, graph-distance-2 correlators, and graph-distance-3 correlators.

The frozen upstream QAT repository is pinned as a Git submodule at:

```text
29bf4d07fa3a16c8d280e717780633299da84c27
```

The primary verifier reconstructs the graph and observable geometry directly from that frozen upstream state.

### Independently verified geometry

| Quantity | Verified result |
|---|---:|
| Qubits | 51 |
| Unique graph edges | 56 |
| Edge-layer sizes | 19 / 19 / 18 |
| Degree-2 vertices | 41 |
| Degree-3 vertices | 10 |
| Graph-distance-2 pairs | 71 |
| Graph-distance-3 pairs | **86** |
| Upstream `ZZd3` pair list | **Exact match to graph-derived set** |

The `86`-pair result matters. An early project draft incorrectly recorded 84 pairs. Reconstructing the graph exposed the error, and the upstream README list was then checked against the graph-derived set: 86 unique entries, no omissions, no extras.

A reproducer normalizing the same numerator by 84 instead of 86 would compute a different observable by a factor of `86/84 ≈ 1.02381`—a ~2.4% shift.

### Formal backward support cones

For each of the 86 graph-distance-3 `ZZ` terms, the verifier computes the union of possible Pauli support under backward propagation through the published RX/RZ/RZZ layer ordering.

The calculation is deliberately interpreted narrowly: it is a **support-containment cone**, not a claim that every included qubit contributes materially to the final expectation value.

| Floquet cycles | Minimum cone size | Terms spanning all 51 qubits |
|---:|---:|---:|
| 5 | 28 | 11 / 86 |
| 6 | 32 | 32 / 86 |
| 7 | 39 | 62 / 86 |
| 8 | 45 | 75 / 86 |
| 9 | 50 | 85 / 86 |
| **10** | **51** | **86 / 86** |
| 13 | 51 | 86 / 86 |

**Established conclusion:** by cycle 10, no 16–20-qubit reduction of the reported cycle-13+ observable is justified by simple support containment.

**Not established:** that every qubit contributes significantly, that a small-patch approximation must be numerically poor, or that this says anything directly about the sign or magnitude of the N=51 SPP truncation error.

---

## The convergence question

The reported `ZZ_{d=3}` SPP result is a single point at `W=16, ε₀=5×10⁻⁸`. The live QAT entry supplies no numerical error interval for that classical value.

The relevant published evidence is asymmetric across observables:

| Observable | Reported SPP settings |
|---|---|
| Magnetization | `(W=11, ε₀=1e-11)` and `(W=20, ε₀=1e-9)` |
| `ZZ_{d=2}` | `(W=16, ε₀=1e-9)` |
| `ZZ_{d=3}` | `(W=16, ε₀=5e-8)` — single setting |

At cycle 16, the two published magnetization SPP settings give:

```text
(W=11, ε₀=1e-11)  ->  0.41110594
(W=20, ε₀=1e-9)   ->  0.38697176
```

Their difference is:

```text
0.02413418
```

The QESEM interval half-width at the same cycle is:

```text
0.02130
```

So the published SPP parameter sensitivity in the one observable with a two-setting comparison is about **1.133× the quoted QESEM half-width**.

This does not prove that `ZZ_{d=3}` is unconverged, nor does it prove the reported `0.183429` is biased in any particular direction. It establishes a more limited evidentiary question: **what same-instance convergence evidence supports the single reported `ZZ_{d=3}` point?**

A direct answer would be a controlled sweep in `ε₀` and, separately, `W` at fixed cycle count, demonstrating a stable plateau at a scale appropriate to the comparison being made.

The upstream authors already disclose that convincing classical convergence is not achieved in the difficult late-cycle regime. `tnbench` treats that disclosure as part of the evidence, not as something to “discover.”

---

## What tnbench does *not* claim

This boundary is central to the project.

`tnbench` does **not** currently claim that:

- `0.183429` is numerically wrong;
- SPP truncation is necessarily downward-biased;
- the sign pattern of SPP–QESEM residuals proves a truncation mechanism;
- every qubit inside the formal causal cone materially affects the final observable;
- a small-N simulation can quantitatively stand in for the N=51 late-cycle calculation;
- the absence of an SPP error interval is a formal QAT rules violation;
- the circuit parameters were deliberately chosen to defeat sparse-Pauli methods.

Claims that were proposed and later rejected remain visible in the adjudication ledger.

---

## Reproducibility

The primary geometry and causal-cone verification uses only the Python standard library and the pinned upstream QAT submodule.

### Fresh clone

```bash
git clone --recurse-submodules https://github.com/amitb-quantum/tnbench.git
cd tnbench
python scripts/verify_floquet_geometry.py
```

Expected high-level output:

```text
edges:          56
degrees:        {2: 41, 3: 10}
ZZd3 pairs:     86
README match:   True

cycles   min cone   full 51q
     5         28    11/86
     6         32    32/86
     7         39    62/86
     8         45    75/86
     9         50    85/86
    10         51    86/86
    13         51    86/86

all 86 full by cycle: 10
```

The verifier writes:

```text
analysis/floquet_geometry_verification.json
```

The output records the pinned upstream SHA, SHA-256 hashes of the QASM and README inputs, graph invariants, pair-set reconciliation, causal-cone table, and executable assumptions used by the support-expansion logic.

### Verify the upstream pin

```bash
cat instances/UPSTREAM_SHA
git -C instances/qat rev-parse HEAD
```

Both should report:

```text
29bf4d07fa3a16c8d280e717780633299da84c27
```

### Optional environment verification

`env/verify_env.py` records the local numerical environment, GPU availability, precision throughput, dtype agreement, and a PEPS memory estimate. The current environment used Quimb/Cotengra/CuPy on an RTX 5090; these packages are **not required** for the primary geometry verifier.

```bash
python env/verify_env.py
```

The corresponding environment snapshot is stored in:

```text
env_verification.json
```

---

## Adjudication discipline

The project follows a stricter rule than “plausible analysis.”

- **No assertion enters as true by default.**
- Load-bearing claims require an executable check, independent re-derivation, or a cited primary source.
- Predictions should be written before the run that tests them.
- Upstream artifacts are pinned by SHA rather than copied and silently modified.
- Machine-readable verification outputs are committed with the reasoning they support.
- Refuted claims remain in the ledger.
- Public comments distinguish verified facts, interpretation, anomalies, and open questions.

This rule has already caught multiple mistakes in the project itself, including:

- an incorrect `84`-pair normalization assumption (`86` is correct);
- an inferred heavy-hex degree split of `17/34` instead of the reconstructed `10/41`;
- an incorrect “near-π/2 RX” interpretation caused by reading the model parameter instead of the actual `RX(θx/3)` gate;
- an invalid proposal to prune intermediate X/Y Pauli components exactly;
- an initial causal-cone table that expanded support one backward layer too early.

Those corrections are part of the artifact, not hidden cleanup.

---

## Adjudication ledger

The main reasoning record is [`notes/ADJUDICATION_LEDGER.md`](notes/ADJUDICATION_LEDGER.md).

It separates claims into statuses such as:

```text
VERIFIED
VERIFIED EXTERNALLY
PARTIAL
UNVERIFIED
REJECTED
FALSE
PROBABLE
NOT ESTABLISHED
CONFOUNDED
```

The ledger records both external findings and our own refuted work, including the exact mechanism behind corrections where known.

The original pre-adjudication hypotheses are retained in [`notes/PROJECT_BRIEF.md`](notes/PROJECT_BRIEF.md) with a pointer to their resolved status rather than being rewritten after the fact.

---

## Repository layout

```text
tnbench/
├── README.md
├── LICENSE
├── analysis/
│   └── floquet_geometry_verification.json
├── env/
│   ├── requirements.txt
│   └── verify_env.py
├── env_verification.json
├── instances/
│   ├── UPSTREAM_SHA
│   └── qat/                         # pinned QAT git submodule
├── notes/
│   ├── ADJUDICATION_LEDGER.md
│   ├── DRAFT_COMMENTS.md
│   └── PROJECT_BRIEF.md
└── scripts/
    └── verify_floquet_geometry.py
```

---

## Source-value anomaly under review

A separate, narrower source-data question exists for the `ZZ_{d=2}` SPP series. The upstream table reports `0.250253` at both cycle 16 and cycle 29 to six decimals, with different runtimes (`31,559 s` vs `42,506 s`). The cycle-29 point also sits away from the neighboring cycle-26 and cycle-30 values.

This is recorded as a **verified anomaly**, not a proven transcription error. Confirmation requires the underlying result artifact or submitter clarification.

Relevant QAT submission: [issue #168](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/168).

---

## Public-review posture

The intended public-review posture is deliberately conservative:

- ask for source-value confirmation where a source anomaly exists;
- ask for convergence evidence where convergence is not externally assessable;
- do not assert that a numerical result is wrong without evidence;
- update the ledger plainly if submitters provide evidence that resolves an open question.

Draft comments are kept in [`notes/DRAFT_COMMENTS.md`](notes/DRAFT_COMMENTS.md) and are frozen before posting.

---

## References

- [Quantum Advantage Tracker](https://quantum-advantage-tracker.github.io/)
- [QAT repository](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io)
- [SPP/ORQA `ZZd3` submission — QAT #171](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/171)
- [SPP/ORQA `ZZd2` submission — QAT #168](https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/168)
- Broers, Sun & Yunoki, **Scalable simulation of quantum many-body dynamics with OR-represented quantum algebra**, arXiv:2506.13241; accepted in *Physical Review Applied* (2026).

---

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
