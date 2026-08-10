#!/usr/bin/env python3

import ast
import hashlib
import json
import math
import re
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = (
    ROOT
    / "instances"
    / "qat"
    / "data"
    / "observable-estimations"
    / "circuit-models"
    / "floquet_mixed_field_ising"
)

QASM = MODEL_DIR / "floquet_mixed_field_ising_zzd3_51qx16c.qasm"
README = MODEL_DIR / "README.md"
UPSTREAM_SHA = ROOT / "instances" / "UPSTREAM_SHA"
OUTPUT = ROOT / "analysis" / "floquet_geometry_verification.json"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_first_cycle_edge_layers(qasm_text):
    """
    Recover E1, E2, E3 directly from the first three RZZ/barrier
    groups in the frozen QASM.
    """
    groups = []
    current = []

    pat = re.compile(
        r"^rzz\(pi/3\)\s+q\[(\d+)\],\s*q\[(\d+)\];$"
    )

    for raw in qasm_text.splitlines():
        line = raw.strip()

        m = pat.match(line)
        if m:
            current.append((int(m.group(1)), int(m.group(2))))
            continue

        if line.startswith("barrier "):
            if current:
                groups.append(tuple(current))
                current = []

                if len(groups) == 3:
                    break

    assert len(groups) == 3, f"expected 3 edge layers, got {len(groups)}"

    sizes = tuple(len(g) for g in groups)
    assert sizes == (19, 19, 18), f"unexpected layer sizes: {sizes}"

    return groups


def parse_readme_zzd3_pairs(readme_text):
    """
    Parse the first N=51 ZZ_{d=3} pair-list row from the frozen README.
    """
    for raw in readme_text.splitlines():
        if "$ZZ_{d=3}$" in raw and "[[" in raw:
            cells = raw.split("|")
            if len(cells) >= 3:
                pairs = ast.literal_eval(cells[2].strip())
                return [tuple(sorted(map(int, p))) for p in pairs]

    raise RuntimeError("could not locate N=51 ZZ_{d=3} pair list")


def build_graph(edge_layers):
    adj = {i: set() for i in range(51)}
    all_edges = set()

    for layer in edge_layers:
        for a, b in layer:
            edge = tuple(sorted((a, b)))
            assert edge not in all_edges, f"duplicate edge: {edge}"
            all_edges.add(edge)

            adj[a].add(b)
            adj[b].add(a)

    return adj, all_edges


def all_pairs_at_distance(adj, target_distance):
    result = set()

    for source in range(51):
        dist = {source: 0}
        q = deque([source])

        while q:
            u = q.popleft()

            if dist[u] >= target_distance:
                continue

            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)

        for target in range(source + 1, 51):
            if dist.get(target) == target_distance:
                result.add((source, target))

    return result


def expand_support(support, edge_layer):
    """
    Union-of-possible-support causal expansion through one disjoint
    RZZ edge layer.

    Once transverse X/Y components are available, an RZZ gate with
    exactly one endpoint in the current support can generate support
    on its other endpoint in at least one Pauli branch.
    """
    support = set(support)
    added = set()

    for a, b in edge_layer:
        if (a in support) ^ (b in support):
            added.add(a)
            added.add(b)

    return support | added


def backward_cone(pair, cycles, e1, e2, e3):
    """
    Formal union-of-possible-Pauli-support cone.

    Forward ordering per Floquet cycle is:
        U1 -> U2 -> U3

    and each Um is:
        RX -> RZ -> RZZ(Em)

    Therefore backward ordering is:
        E3 RZZ -> RZ -> RX
        E2 RZZ -> RZ -> RX
        E1 RZZ -> RZ -> RX

    At the terminal observable, the Pauli is purely Z, so the first
    backward RZZ layer cannot enlarge support. After crossing the first
    RX layer, sin(theta_x/3) != 0 guarantees a transverse branch on each
    supported qubit. Thereafter, an incident RZZ with
    sin(theta_zz) != 0 can enlarge the union-of-possible-support cone.

    This is a formal support-containment cone, not a statement that every
    included qubit contributes materially to the final expectation.
    """
    support = set(pair)
    transverse_ready = False

    for _ in range(cycles):
        for layer in (e3, e2, e1):
            if transverse_ready:
                support = expand_support(support, layer)

            # Backward propagation now crosses RZ then RX. Since
            # sin(theta_x/3) != 0, every supported Z component has a
            # nonzero transverse branch before the next RZZ layer.
            transverse_ready = True

    return support


def canonical_pair_hash(pairs):
    payload = "\n".join(f"{a},{b}" for a, b in sorted(pairs))
    return hashlib.sha256(payload.encode()).hexdigest()


qasm_text = QASM.read_text()
readme_text = README.read_text()

# Support-expansion assumptions used by backward_cone().
# These values are taken from the frozen QASM instance.
rx_match = re.search(r"^rx\(([^)]+)\)", qasm_text, re.MULTILINE)
if not rx_match:
    raise RuntimeError("could not parse RX angle from QASM")

theta_x_over_3 = float(rx_match.group(1))
theta_zz = math.pi / 3

assert abs(math.sin(theta_x_over_3)) > 1e-12, (
    "RX angle has zero sine; transverse support is not generated"
)
assert abs(math.sin(theta_zz)) > 1e-12, (
    "RZZ angle has zero sine; support cannot expand across RZZ edges"
)

e1, e2, e3 = parse_first_cycle_edge_layers(qasm_text)

adj, all_edges = build_graph((e1, e2, e3))

degree_hist = Counter(len(adj[i]) for i in range(51))

assert len(all_edges) == 56
assert degree_hist == Counter({2: 41, 3: 10}), degree_hist

derived_d3 = all_pairs_at_distance(adj, 3)
readme_d3_list = parse_readme_zzd3_pairs(readme_text)
readme_d3 = set(readme_d3_list)

assert len(derived_d3) == 86
assert len(readme_d3_list) == 86
assert len(readme_d3) == 86
assert derived_d3 == readme_d3

cone_table = []

for cycles in range(1, 17):
    sizes = [
        len(backward_cone(pair, cycles, e1, e2, e3))
        for pair in sorted(derived_d3)
    ]

    cone_table.append(
        {
            "cycles": cycles,
            "min_cone_size": min(sizes),
            "max_cone_size": max(sizes),
            "full_51_count": sum(size == 51 for size in sizes),
            "pair_count": len(sizes),
        }
    )

first_full_cycle = next(
    row["cycles"]
    for row in cone_table
    if row["full_51_count"] == 86
)

assert first_full_cycle == 10

expected_checkpoints = {
    5: (28, 11),
    6: (32, 32),
    7: (39, 62),
    8: (45, 75),
    9: (50, 85),
    10: (51, 86),
    13: (51, 86),
}

for cycles, (expected_min, expected_full) in expected_checkpoints.items():
    row = next(r for r in cone_table if r["cycles"] == cycles)

    assert row["min_cone_size"] == expected_min, (
        cycles,
        row,
        expected_min,
    )
    assert row["full_51_count"] == expected_full, (
        cycles,
        row,
        expected_full,
    )

result = {
    "schema": "tnbench.floquet_geometry_verification.v1",
    "upstream_sha": UPSTREAM_SHA.read_text().strip(),
    "inputs": {
        "qasm": {
            "path": str(QASM.relative_to(ROOT)),
            "sha256": sha256_file(QASM),
        },
        "readme": {
            "path": str(README.relative_to(ROOT)),
            "sha256": sha256_file(README),
        },
    },
    "edge_layers": {
        "E1": len(e1),
        "E2": len(e2),
        "E3": len(e3),
        "total_unique_edges": len(all_edges),
    },
    "degree_histogram": {
        str(k): v for k, v in sorted(degree_hist.items())
    },
    "distance_3_pairs": {
        "graph_derived_count": len(derived_d3),
        "readme_count": len(readme_d3_list),
        "readme_unique_count": len(readme_d3),
        "sets_equal": derived_d3 == readme_d3,
        "canonical_sha256": canonical_pair_hash(derived_d3),
    },
    "causal_cone": {
        "definition": (
            "union of possible backward Pauli support; expansion begins "
            "only after backward propagation crosses the first RX layer"
        ),
        "assumptions": {
            "theta_x_over_3": theta_x_over_3,
            "sin_theta_x_over_3_nonzero": abs(math.sin(theta_x_over_3)) > 1e-12,
            "theta_zz": theta_zz,
            "sin_theta_zz_nonzero": abs(math.sin(theta_zz)) > 1e-12,
        },
        "first_cycle_all_86_pairs_span_51": first_full_cycle,
        "table": cone_table,
    },
    "assertions": {
        "edge_count_56": True,
        "degree_histogram_10_deg3_41_deg2": True,
        "distance3_pair_count_86": True,
        "readme_pair_set_matches_graph": True,
        "all_distance3_cones_span_51_by_cycle_10": True,
    },
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(result, indent=2) + "\n")

print("Floquet geometry verification")
print("-----------------------------")
print(f"edges:          {len(all_edges)}")
print(f"degrees:        {dict(sorted(degree_hist.items()))}")
print(f"ZZd3 pairs:     {len(derived_d3)}")
print(f"README match:   {derived_d3 == readme_d3}")
print()
print("cycles   min cone   full 51q")
for row in cone_table:
    if row["cycles"] in expected_checkpoints:
        print(
            f'{row["cycles"]:>6}   '
            f'{row["min_cone_size"]:>8}   '
            f'{row["full_51_count"]:>3}/86'
        )
print()
print(f"all 86 full by cycle: {first_full_cycle}")
print(f"written: {OUTPUT.relative_to(ROOT)}")
