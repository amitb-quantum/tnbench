#!/usr/bin/env python3
"""
patch_memory_model.py -- replace the section-5 memory model in verify_env.py.

Why: the original block printed a chi^2 boundary-MPS column and called it
the binding constraint. chi^2 is the EXACT-contraction bond, which no real
implementation carries; boundary-MPS truncates to a chosen chi_b. The block
therefore reported a worst-case ceiling as an operating cost.

Behaviour:
  - locates the block by anchor lines, not by exact whole-block match
  - refuses to run if anchors are missing or ambiguous
  - writes a timestamped backup before touching anything
  - syntax-checks the result and rolls back if it fails
  - idempotent: detects an already-patched file and exits cleanly

Usage:
    python patch_memory_model.py [path/to/verify_env.py]
Default path: ./verify_env.py
"""

import ast
import shutil
import sys
from datetime import datetime
from pathlib import Path

START_ANCHOR = "assumed patch:"
END_ANCHOR = "is the binding constraint."
PATCH_MARKER = "chi_b is a second truncation"

NEW_BLOCK = '''print(f"  assumed patch: {N_DEG3} degree-3 sites, {N_DEG2} degree-2 sites, phys dim 2")
print()
print("  State memory (GPU-resident, complex64):")
for chi_ in (32, 64, 128, 192, 256):
    s64 = (N_DEG3 * 2 * chi_**3 + N_DEG2 * 2 * chi_**2) * 8 / 1024**3
    print(f"    chi={chi_:<5} {s64:7.2f} GiB")

print()
print("  Boundary-MPS memory depends on chi_b, a CHOSEN truncation --")
print("  not on chi^2. chi_b = chi^2 is the exact (never-used) limit.")
print()
print(f"    {'chi':>5} {'chi_b':>7} {'bMPS tensor':>14}")
for chi_ in (64, 128, 192):
    for chi_b in (chi_ // 2, chi_, 2 * chi_):
        gib = (chi_b**2) * (chi_**2) * 8 / 1024**3
        print(f"    {chi_:>5} {chi_b:>7} {gib:>11.2f} GiB")

print()
print("  chi_b is a second truncation with its own unbounded error.")
print("  Submissions report chi. They often do not report chi_b or its")
print("  convergence evidence. That gap is the review question.")'''


def find_unique(lines, needle, label):
    hits = [i for i, ln in enumerate(lines) if needle in ln]
    if not hits:
        sys.exit(f"ERROR: {label} anchor not found: {needle!r}\n"
                 f"       File may already be edited. Inspect manually.")
    if len(hits) > 1:
        sys.exit(f"ERROR: {label} anchor appears {len(hits)} times: {needle!r}\n"
                 f"       Ambiguous. Refusing to patch.")
    return hits[0]


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "verify_env.py")
    if not path.is_file():
        sys.exit(f"ERROR: no such file: {path}")

    original = path.read_text()

    if PATCH_MARKER in original:
        print(f"Already patched: {path}")
        print("Nothing to do.")
        return 0

    lines = original.splitlines()
    start = find_unique(lines, START_ANCHOR, "start")
    end = find_unique(lines, END_ANCHOR, "end")

    if end <= start:
        sys.exit("ERROR: end anchor precedes start anchor. Refusing to patch.")

    # preserve the indentation of the first replaced line (should be col 0)
    indent = lines[start][: len(lines[start]) - len(lines[start].lstrip())]
    new_lines = [indent + ln if ln.strip() else ln
                 for ln in NEW_BLOCK.splitlines()]

    patched = "\n".join(lines[:start] + new_lines + lines[end + 1:])
    if original.endswith("\n"):
        patched += "\n"

    # syntax gate before writing anything irreversible
    try:
        ast.parse(patched)
    except SyntaxError as e:
        sys.exit(f"ERROR: patched source does not parse: {e}\nNo changes written.")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak_{stamp}")
    shutil.copy2(path, backup)
    path.write_text(patched)

    removed = end - start + 1
    added = len(new_lines)
    print(f"Patched : {path}")
    print(f"Backup  : {backup}")
    print(f"Lines   : -{removed} +{added}  (block at lines {start + 1}-{end + 1})")
    print()
    print("Verify with:  python", path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
