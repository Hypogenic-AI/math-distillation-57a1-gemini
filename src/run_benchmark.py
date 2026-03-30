#!/usr/bin/env python3
"""Run a small benchmark for Stage-1 implication decisions."""

from __future__ import annotations

import json
import math
import os
import statistics
import time
from dataclasses import dataclass
from typing import Dict, List

import matplotlib.pyplot as plt

from implication_solver import solve_implication


@dataclass
class Case:
    e1: str
    e2: str
    label: bool
    note: str


CASES: List[Case] = [
    Case("x = x*y", "x = x*x", True, "Substitute y:=x"),
    Case("x = y*x", "x = x*x", True, "Substitute y:=x"),
    Case("x*y = x", "x*x = x", True, "Substitute y:=x"),
    Case("x*y = y", "x*x = x", True, "Substitute y:=x"),
    Case("x*(y*z) = (x*y)*z", "(x*x)*x = x*(x*x)", True, "Associativity instance"),
    Case("x = y", "x*x = y*y", True, "Congruence"),
    Case("x*x = x", "x*y = x", False, "Idempotent does not force left projection"),
    Case("x*y = y*x", "x*y = x", False, "Commutative does not force left projection"),
    Case("(x*y)*z = x*(y*z)", "x*y = x", False, "Associativity does not force left projection"),
    Case("x*y = x", "x = y*x", False, "Left projection does not imply x=y"),
]


def wilson_interval(k: int, n: int, z: float = 1.96) -> List[float]:
    if n == 0:
        return [0.0, 1.0]
    p = k / n
    den = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / den
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / den
    return [center - margin, center + margin]


def main() -> None:
    os.makedirs("results/plots", exist_ok=True)

    rows: List[Dict[str, object]] = []
    for c in CASES:
        t0 = time.perf_counter()
        pred = solve_implication(c.e1, c.e2, max_order=3, max_depth=2, sub_limit=8)
        dt = time.perf_counter() - t0
        rows.append(
            {
                "e1": c.e1,
                "e2": c.e2,
                "label": c.label,
                "prediction": pred["answer"],
                "correct": bool(pred["answer"] == c.label),
                "mode": pred["mode"],
                "runtime_sec": dt,
                "note": c.note,
                "countermodel": pred.get("countermodel"),
            }
        )

    n = len(rows)
    correct = sum(1 for r in rows if r["correct"])
    acc = correct / n

    always_true_correct = sum(1 for r in rows if r["label"] is True)
    countermodel_only_correct = sum(
        1 for r in rows if ((r["mode"] == "countermodel") == (r["label"] is False))
    )

    runtimes = [float(r["runtime_sec"]) for r in rows]

    metrics = {
        "n_cases": n,
        "accuracy": acc,
        "accuracy_wilson_95": wilson_interval(correct, n),
        "mean_runtime_sec": statistics.mean(runtimes),
        "median_runtime_sec": statistics.median(runtimes),
        "baseline_always_true_accuracy": always_true_correct / n,
        "baseline_countermodel_only_accuracy": countermodel_only_correct / n,
        "evidence_mode_counts": {
            "countermodel": sum(1 for r in rows if r["mode"] == "countermodel"),
            "bounded_derivation": sum(1 for r in rows if r["mode"] == "bounded_derivation"),
            "no_countermodel_up_to_bound": sum(
                1 for r in rows if r["mode"] == "no_countermodel_up_to_bound"
            ),
        },
    }

    with open("results/predictions.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    with open("results/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ["Always True", "Countermodel Only", "Hybrid"]
    values = [
        metrics["baseline_always_true_accuracy"],
        metrics["baseline_countermodel_only_accuracy"],
        metrics["accuracy"],
    ]
    ax.bar(labels, values, color=["#888888", "#4c78a8", "#2ca02c"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Accuracy")
    ax.set_title("Stage-1 Decision Accuracy on Curated Benchmark")
    for i, v in enumerate(values):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center")
    fig.tight_layout()
    fig.savefig("results/plots/accuracy_comparison.png", dpi=150)

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.hist(runtimes, bins=min(8, len(runtimes)), color="#f58518", edgecolor="black")
    ax2.set_xlabel("Runtime (seconds)")
    ax2.set_ylabel("Count")
    ax2.set_title("Per-Query Runtime Distribution")
    fig2.tight_layout()
    fig2.savefig("results/plots/runtime_hist.png", dpi=150)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
