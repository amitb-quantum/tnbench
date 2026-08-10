# Draft public comments — QAT observable-estimations

Status: FROZEN PRE-PUBLICATION — 2026-08-10.

Purpose: preserve the exact first public comment and posting sequence before publication. Do not edit this frozen text after posting without recording the change separately.

## Posting sequence

1. Post the convergence-evidence comment below on QAT issue #168.
2. Stop after the first post and allow responses to shape any follow-up.
3. Do not post to #171 or raise the PR #230 / cycle-29 duplicate-value question on the same day.
4. If submitters provide a same-instance convergence sweep, update the adjudication ledger plainly and acknowledge the evidence publicly.

Important venue distinction: #168 is **not** the correct venue for the cycle-29 duplicate-value anomaly; that row was introduced in PR #230. #168 *is* an appropriate venue for the convergence question below because it is the open SPP/ORQA `ZZ_{d=2}` submission at `W=16, ε₀=1e-9`, with no submitted low/high error bounds.

---

## Comment 1 — QAT issue #168

**Venue:** https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/issues/168

**Purpose:** independent geometry verification plus a direct, non-accusatory request for convergence evidence for the SPP truncation settings.

> Independent geometry verification, and a question on convergence evidence for this entry.
>
> I reconstructed the 51-qubit heavy-hex graph and the ZZ_{d=2} / ZZ_{d=3} observables directly from the frozen upstream edge lists, and can confirm the published geometry: 56 edges (19/19/18), degree histogram {2: 41, 3: 10}, 71 distance-2 pairs, 86 distance-3 pairs, and the README pair lists match the graph-derived sets exactly. Verifier and machine-readable output: https://github.com/amitb-quantum/tnbench/tree/v0.1.0-adjudication — standard library only, reproduces from a clean clone in two commands.
>
> My question is about the convergence evidence for the SPP truncation settings, since the error-bound fields on this submission are blank.
>
> For magnetization at cycle 16 the README reports two SPP settings: (W=11, ε₀=1e-11) → 0.41110594 and (W=20, ε₀=1e-9) → 0.38697176. Those differ by 0.02413, which is about 1.13× the QESEM interval half-width of 0.02130 at the same cycle. So on the one observable where a two-setting comparison is published, the parameter sensitivity exceeds the quantum estimator's quoted uncertainty.
>
> This entry (ZZ_{d=2}) reports a single setting, W=16, ε₀=1e-9, and ZZ_{d=3} reports a single setting at ε₀=5e-8. Is there a same-instance sweep — tightening ε₀, and separately increasing W, at fixed cycle count — that shows these values on a plateau? A plateau narrower than the QESEM half-width would settle it; continued drift under tightening would be equally informative.
>
> To be clear, I'm not suggesting the reported values are incorrect. I'm asking what convergence evidence is available, given that the README notes convincing classical convergence is not achieved in the late-cycle regime and the ORQA methodology treats truncation accuracy as system-dependent.

---

## Deferred follow-ups

### QAT #171

Do not post on the same day as Comment 1. #171 is the closed `ZZ_{d=3}` SPP/ORQA submission (`0.183429`, `W=16`, `ε₀=5e-8`) and carries project status `Verified`. If a follow-up is needed, first incorporate any response on #168. Do not assume that `Verified` means scientific certification of convergence; ask what the status establishes if that remains relevant.

### PR #230 / cycle-29 ZZd2 anomaly

Do not post on the same day as Comment 1. The cycle-29 `ZZ_{d=2}` SPP value `0.250253` was introduced in PR #230 and duplicates the cycle-16 value to six decimals while reporting a different runtime. This remains a verified anomaly, not a proven transcription error. If raised later, use PR #230 provenance or a fresh data-quality issue rather than #168.

---

## Tone rules

- No claim that any reported SPP value is wrong.
- No claim of downward truncation bias.
- No one-sided residual argument.
- No schema-violation accusation.
- No speculation about parameter intent.
- Distinguish `No response` / unavailable bounds from a demonstrated zero uncertainty.
- If new evidence resolves the question, update the ledger and say so plainly.
