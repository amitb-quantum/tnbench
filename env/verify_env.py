#!/usr/bin/env python3
"""
verify_env.py -- Environment gate for classical tensor-network benchmarking.

Answers four questions before any real work starts:
  1. Are the packages present and importable?
  2. Does the GPU exist, and how much usable VRAM?
  3. What is the actual fp64:fp32 penalty on this card?
  4. Do complex64 and complex128 agree at small size?

Question 4 is the important one. If complex64 does not reproduce
complex128 to acceptable tolerance on a small contraction, then no
large-chi complex64 result from this machine is trustworthy, and that
must be recorded as an environment limit rather than discovered later.

Run:  python verify_env.py
Exit: 0 = all gates passed, 1 = at least one gate failed or skipped
"""

import json
import platform
import sys
import time
from datetime import datetime, timezone

RESULTS = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "host": platform.node(),
    "python": sys.version.split()[0],
    "gates": {},
}

SEP = "-" * 68


def gate(name, ok, detail=""):
    RESULTS["gates"][name] = {"pass": bool(ok), "detail": detail}
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {name}" + (f"  {detail}" if detail else ""))
    return ok


# ----------------------------------------------------------------------
# 1. Packages
# ----------------------------------------------------------------------
print(SEP)
print("1. PACKAGE INVENTORY")
print(SEP)

versions = {}
for mod in ("numpy", "scipy", "quimb", "cotengra", "autoray", "opt_einsum", "cupy"):
    try:
        m = __import__(mod)
        v = getattr(m, "__version__", "unknown")
        versions[mod] = v
        print(f"  {mod:<12} {v}")
    except ImportError:
        versions[mod] = None
        print(f"  {mod:<12} -- not installed")

RESULTS["versions"] = versions
core = ("numpy", "quimb", "cotengra")
gate("core_packages", all(versions[m] for m in core),
     "quimb + cotengra + numpy required")

try:
    import kahypar  # noqa: F401
    print("  kahypar      present (better contraction paths)")
    RESULTS["kahypar"] = True
except ImportError:
    print("  kahypar      absent  (cotengra falls back to slower path search)")
    RESULTS["kahypar"] = False


# ----------------------------------------------------------------------
# 2. GPU presence and VRAM
# ----------------------------------------------------------------------
print()
print(SEP)
print("2. GPU")
print(SEP)

cp = None
try:
    import cupy as cp
    dev = cp.cuda.Device(0)
    free_b, total_b = dev.mem_info
    props = cp.cuda.runtime.getDeviceProperties(0)
    name = props["name"].decode() if isinstance(props["name"], bytes) else props["name"]
    cc = f"{props['major']}.{props['minor']}"
    print(f"  device        {name}")
    print(f"  compute cap   sm_{props['major']}{props['minor']}  (CC {cc})")
    print(f"  VRAM total    {total_b / 1024**3:.1f} GiB")
    print(f"  VRAM free     {free_b / 1024**3:.1f} GiB")
    RESULTS["gpu"] = {
        "name": name, "cc": cc,
        "vram_total_gib": round(total_b / 1024**3, 2),
        "vram_free_gib": round(free_b / 1024**3, 2),
    }
    gate("gpu_available", True, name)
except Exception as e:
    cp = None
    RESULTS["gpu"] = None
    gate("gpu_available", False, f"{type(e).__name__}: {e}")


# ----------------------------------------------------------------------
# 3. fp64 vs fp32 throughput
# ----------------------------------------------------------------------
print()
print(SEP)
print("3. PRECISION THROUGHPUT  (consumer Blackwell fp64 is heavily throttled)")
print(SEP)


def bench_matmul(xp, dtype, n=4096, reps=3, sync=None):
    a = xp.ones((n, n), dtype=dtype)
    b = xp.ones((n, n), dtype=dtype)
    xp.matmul(a, b)          # warm up / allocate
    if sync:
        sync()
    t0 = time.perf_counter()
    for _ in range(reps):
        xp.matmul(a, b)
    if sync:
        sync()
    dt = (time.perf_counter() - t0) / reps
    # complex matmul ~ 4x the real flop count
    mult = 4.0 if xp.dtype(dtype).kind == "c" else 1.0
    gflops = mult * 2.0 * n**3 / dt / 1e9
    del a, b
    return dt, gflops


if cp is not None:
    try:
        sync = cp.cuda.Stream.null.synchronize
        r32 = bench_matmul(cp, cp.complex64, sync=sync)
        r64 = bench_matmul(cp, cp.complex128, sync=sync)
        ratio = r64[0] / r32[0]
        print(f"  complex64     {r32[1]:9.1f} GFLOP/s   ({r32[0]*1e3:.1f} ms)")
        print(f"  complex128    {r64[1]:9.1f} GFLOP/s   ({r64[0]*1e3:.1f} ms)")
        print(f"  penalty       {ratio:.1f}x slower in double precision")
        RESULTS["precision"] = {
            "c64_gflops": round(r32[1], 1),
            "c128_gflops": round(r64[1], 1),
            "penalty_x": round(ratio, 1),
        }
        if ratio > 8:
            print("  -> Run production sweeps in complex64. Reserve complex128")
            print("     for small-chi CPU cross-checks only.")
        gate("precision_measured", True, f"{ratio:.1f}x fp64 penalty")
    except Exception as e:
        gate("precision_measured", False, str(e))
else:
    print("  skipped (no GPU)")
    gate("precision_measured", False, "no GPU")


# ----------------------------------------------------------------------
# 4. complex64 vs complex128 agreement  -- the gate that matters
# ----------------------------------------------------------------------
print()
print(SEP)
print("4. DTYPE AGREEMENT  (does single precision reproduce double?)")
print(SEP)

import numpy as np

rng = np.random.default_rng(20260810)
chi, d = 64, 4
# a small chain contraction standing in for a real TN sweep
tensors128 = [
    (rng.standard_normal((chi, d, chi)) + 1j * rng.standard_normal((chi, d, chi))
     ).astype(np.complex128) / np.sqrt(chi * d)
    for _ in range(12)
]


def contract_chain(ts, dtype, xp=np):
    """Sweep an MPS transfer operator: E <- sum_p A_p^dag E A_p.

    Bond dimension stays fixed at chi, so this is a faithful stand-in for a
    real sweep -- rounding error accumulates over sites exactly the way it
    does in production, without the memory blowup of a naive chain product.
    """
    E = xp.eye(chi, dtype=dtype)
    for t in ts:
        A = xp.asarray(t.astype(dtype))
        acc = xp.zeros((chi, chi), dtype=dtype)
        for p in range(A.shape[1]):
            Ap = A[:, p, :]
            acc = acc + Ap.conj().T @ E @ Ap
        E = acc / xp.linalg.norm(acc)
    return E


v128 = contract_chain(tensors128, np.complex128)
v64 = contract_chain(tensors128, np.complex64)
num = float(np.linalg.norm(v128 - v64.astype(np.complex128)))
den = float(np.linalg.norm(v128))
rel = num / den if den else float("nan")

print(f"  relative deviation (CPU c64 vs c128):  {rel:.3e}")
RESULTS["dtype_agreement_cpu"] = rel
gate("dtype_agreement_cpu", rel < 1e-4, f"rel={rel:.2e}, threshold 1e-4")

if cp is not None:
    try:
        vg = contract_chain(tensors128, np.complex64, xp=cp)
        vg = cp.asnumpy(vg)
        relg = float(np.linalg.norm(v128 - vg.astype(np.complex128))) / den
        print(f"  relative deviation (GPU c64 vs CPU c128): {relg:.3e}")
        RESULTS["dtype_agreement_gpu"] = relg
        gate("dtype_agreement_gpu", relg < 1e-4, f"rel={relg:.2e}")
    except Exception as e:
        gate("dtype_agreement_gpu", False, str(e))


# ----------------------------------------------------------------------
# 5. Analytic memory model for heavy-hex PEPS
# ----------------------------------------------------------------------
print()
print(SEP)
print("5. MEMORY MODEL  -- heavy-hex PEPS, estimate only, verify empirically")
print(SEP)

# 51-qubit heavy-hex patch: rough split of degree-3 vertex vs degree-2 edge sites
N_DEG3, N_DEG2 = 10, 41
print(f"  assumed patch: {N_DEG3} degree-3 sites, {N_DEG2} degree-2 sites, phys dim 2")
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
print("  convergence evidence. That gap is the review question.")

# ----------------------------------------------------------------------
print()
print(SEP)
passed = sum(1 for g in RESULTS["gates"].values() if g["pass"])
total = len(RESULTS["gates"])
print(f"GATES: {passed}/{total} passed")
print(SEP)

out = "env_verification.json"
with open(out, "w") as f:
    json.dump(RESULTS, f, indent=2)
print(f"Written: {out}")

sys.exit(0 if passed == total else 1)
