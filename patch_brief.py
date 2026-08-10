#!/usr/bin/env python3
"""
patch_brief.py -- update notes/PROJECT_BRIEF.md after the C1-C5 adjudication.

Three edits, none destructive:
  1. Immediate question: truncation-bias -> convergence-evidence framing.
  2. Section 2.3: record N_d3 = 86 WITH provenance (works whether the file
     still says 84 or has already been silently corrected to 86).
  3. Section 3: add a resolution banner. C1-C5 kept VERBATIM for provenance.

Each edit carries one or more acceptable anchor forms. All anchors are
validated before anything is written. Idempotent; timestamped backup.

Usage: python patch_brief.py [path/to/PROJECT_BRIEF.md]
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

MARKER = "RESOLVED — see notes/ADJUDICATION_LEDGER.md"

OBS = "`ZZ_d3 = (1/N_d3) \u03a3_{(i,j): d(i,j)=3} Z_i Z_j`, averaged over the\n"

EDITS = [
    (
        "immediate question",
        (
            "**Immediate question.** Is the SPP (ORQA) entry for\n"
            "`floquet_mixed_field_ising_zzd3_51qx16c` converged, or is it a\n"
            "truncation-biased estimate presented without a convergence study?",
        ),
        "**Immediate question.** Is sufficient convergence evidence reported to\n"
        "treat the SPP/ORQA value for `floquet_mixed_field_ising_zzd3_51qx16c`\n"
        "as a quantitatively controlled classical comparator?\n"
        "\n"
        "(Superseded framing, retained for provenance: the original question\n"
        "asked whether the entry was *truncation-biased*. That framing was\n"
        "dropped \u2014 see C1c in the ledger. No claim that 0.183429 is incorrect\n"
        "is made or required.)",
    ),
    (
        "pair count",
        (
            OBS + "84-pair list given in the upstream README.",
            OBS + "86-pair list given in the upstream README.",
        ),
        "`ZZ_d3 = (1/N_d3) \u03a3_{(i,j): d(i,j)=3} Z_i Z_j`, with **N_d3 = 86**,\n"
        "averaged over the 86-pair list given in the upstream README.\n"
        "\n"
        "Independently confirmed: reconstructing the 51-node graph from the\n"
        "upstream edge layers yields 86 unordered distance-3 pairs, and the\n"
        "README list contains 86 unique entries matching that set exactly.\n"
        "An earlier draft of this brief said 84 \u2014 see F1 in the ledger. A\n"
        "reproducer normalising by 84 computes a different observable\n"
        "(a 2.4% shift, comparable to several residuals under discussion).",
    ),
    (
        "section 3 header",
        (
            "## 3. Contested claims \u2014 asserted by Claude, NOT verified\n"
            "\n"
            "Each needs independent derivation or an executable check. Do not treat\n"
            "any as established.",
        ),
        "## 3. Contested claims \u2014 asserted by Claude, NOT verified\n"
        "\n"
        "> **RESOLVED \u2014 see notes/ADJUDICATION_LEDGER.md for current status.**\n"
        "> C1\u2013C5 are kept verbatim below as the original hypotheses, for\n"
        "> provenance. Outcome in brief: C1 count VERIFIED but its mechanism\n"
        "> REJECTED; C2's RZZ observation VERIFIED, its RX \"near-Clifford\"\n"
        "> claim FALSE; C3 PARTIAL (5/7); C4 FALSE; C5 REJECTED on the narrow\n"
        "> support-containment ground only. Do not cite this section as\n"
        "> current.\n"
        "\n"
        "Each needs independent derivation or an executable check. Do not treat\n"
        "any as established.",
    ),
]


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "notes/PROJECT_BRIEF.md")
    if not path.is_file():
        sys.exit(f"ERROR: no such file: {path}")

    text = path.read_text()

    if MARKER in text:
        print(f"Already patched: {path}\nNothing to do.")
        return 0

    chosen = {}
    for label, alts, _new in EDITS:
        if any(text.count(a) > 1 for a in alts):
            sys.exit(f"ERROR: anchor for '{label}' occurs more than once. "
                     f"Ambiguous; nothing written.")
        hits = [a for a in alts if text.count(a) == 1]
        if not hits:
            sys.exit(f"ERROR: no anchor variant found for '{label}'.\n"
                     f"       File differs from all expected forms. "
                     f"Inspect and patch manually; nothing written.")
        chosen[label] = hits[0]

    for label, _alts, new in EDITS:
        text = text.replace(chosen[label], new)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak_{stamp}")
    shutil.copy2(path, backup)
    path.write_text(text)

    print(f"Patched : {path}")
    print(f"Backup  : {backup}")
    for label, _a, _n in EDITS:
        variant = "84-pair form" if "84-pair" in chosen[label] else (
            "86-pair form" if "86-pair" in chosen[label] else "standard")
        print(f"  applied: {label}" + (f"  ({variant})" if label == "pair count" else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
