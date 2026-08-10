# Draft public comments — QAT observable-estimations

Status: DRAFT. Not posted. Freeze before posting; do not edit after
posting without noting the edit.

Verify before posting:
- [ ] Which issue number is the SPP/ORQA **zzd3** submission (of #171,
      #168, #165). Post on that one, not the ZIZ or mag issue.
- [ ] Re-confirm live tracker still shows `0.183429 [N/A, N/A]`.
- [ ] Re-confirm the ZIZ cycle-16 / cycle-29 duplicate in current
      upstream source (not the rendered README).
- [ ] Repo public, LICENSE present, verifier runs clean from a fresh
      clone.

---

## Comment 1 — post first, separately

**Venue:** the ZIZ (ZZd2) submission issue.
**Purpose:** a factual correction, useful to the submitters, low risk.
Establishes that we read the submission carefully before asking anything
harder.

> Possible transcription issue in the ZIZ late-cycle SPP values.
>
> In the current `floquet_mixed_field_ising` README, the SPP (W=16,
> ε₀=1e-9) entry for ZIZ reads 0.250253 at cycle 16 and again 0.250253
> at cycle 29 — identical to six decimals, with different runtimes
> (31,559 s vs 42,506 s).
>
> The cycle-29 value also breaks the local trend: 0.2355 at cycle 26 and
> 0.23 at cycle 30 bracket it.
>
> Could you confirm the cycle-29 number against the underlying result
> artifact? If it is a copy from the cycle-16 row it would be worth
> correcting; if it is genuine, then disregard.

---

## Comment 2 — post only after Comment 1 has been seen

**Venue:** the SPP/ORQA **zzd3** submission issue.
**Purpose:** the frozen thesis. A request for convergence evidence, not
an assertion that the value is wrong.

> Question on convergence evidence for the ZZ_{d=3} SPP entry.
>
> The tracker lists the SPP/ORQA result for
> `floquet_mixed_field_ising_zzd3_51qx16c` as 0.183429 with [N/A, N/A]
> bounds, at W=16, ε₀=5e-8.
>
> Three things make the convergence status hard to assess from outside:
>
> 1. ZZ_{d=3} is tabulated at a single (W, ε₀) setting. Magnetization
>    has two, ZIZ has one at ε₀=1e-9. ε₀=5e-8 is the loosest threshold
>    reported for this instance.
>
> 2. Where a two-setting comparison does exist — magnetization at cycle
>    16 — the two settings give 0.41111 (W=11, ε₀=1e-11) and 0.38697
>    (W=20, ε₀=1e-9). That is a difference of 0.02413, larger than the
>    QESEM interval half-width of 0.02130 at the same cycle. So on the
>    one observable where truncation sensitivity is visible, it exceeds
>    the quantum estimator's quoted uncertainty.
>
> 3. The README states that neither classical method achieves convincing
>    convergence on this instance, and the ORQA methodology treats
>    truncation accuracy as strongly system-dependent, with systematic
>    ε₀ convergence checks identified as important.
>
> Given that, what convergence evidence supports treating the
> single-setting ZZ_{d=3} value at W=16, ε₀=5e-8 as a quantitatively
> controlled classical comparator?
>
> Concretely, a sweep of ε₀ (and separately W) at fixed cycle count,
> showing a plateau narrower than the QESEM half-width, would settle it
> either way. A drift under tightening would be equally informative.
>
> Separately: we independently reconstructed the 51-qubit heavy-hex
> graph from the published edge layers and confirm the ZZ_{d=3} pair
> list contains 86 distance-3 pairs matching the graph-derived set
> exactly. We also computed formal backward support cones for all 86
> pairs; by cycle 10 every cone spans all 51 qubits, so no small-patch
> reduction is justified by support containment at the cycles reported
> here. Verifier and provenance: <repo URL>

---

## Tone rules

- No claim that 0.183429 is wrong. We do not know that.
- No mention of the one-sided residual pattern. Descriptive only, and
  the cross-observable comparison confounds ε₀ with observable
  difficulty.
- No "schema violation." Evidentiary tension, phrased as a question.
- No speculation about why parameters were chosen.
- If a submitter answers with convergence evidence, the correct public
  response is to say so plainly and update the ledger.
