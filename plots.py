from typing import Any, Optional

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

def plot_lengths(x: list, makespan: list, cp_len: list):
    plt.style.use("seaborn-v0_8-darkgrid")
    _, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, makespan, marker='o', linestyle='-', color='royalblue', markersize=8, linewidth=2, label="Makespan")
    ax.plot(x, cp_len, marker='o', linestyle='-', color='darkorange', markersize=8, linewidth=2, label="CP length")
    ax.grid(True, which="both", linestyle="--", linewidth=0.7, alpha=0.6)

    ax.set_xlabel("Max dependencies", fontsize=12)
    ax.set_ylabel("Average Makespan", fontsize=12)
    ax.set_title("Scheduling performance", fontsize=14, fontweight='bold')
    ax.legend()

    plt.tight_layout()
    plt.savefig("figures/lengths.png")
    plt.show()

def plot_benchmark(x: list[Any], fy: list[Any], sy: Optional[list[Any]] = None, log = False):
    plt.style.use("seaborn-v0_8-darkgrid")
    _, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, fy, marker='.', linestyle='-', color='royalblue', markersize=8, linewidth=2, label="Premier tour")
    if sy is not None:
        ax.plot(x, sy, marker='.', linestyle='-', color='darkorange', markersize=8, linewidth=2, label="Seconde tour")

    ax.grid(True, which="both", linestyle="--", linewidth=0.7, alpha=0.6)

    ax.set_xlabel("#Nodes", fontsize=12)
    ax.set_ylabel("Execution time (s)", fontsize=12)
    ax.set_title("Scheduling performance", fontsize=14, fontweight='bold')
    ax.legend()
    name = "benchmark"
    if log:
        ax.set_xscale("log")
        ax.set_yscale("log")
        name += "log"

    plt.tight_layout()
    plt.savefig(f"figures/{name}.png")
    plt.show()

def plot_schedule(schedule: dict[str, list[dict[str, Any]]]):
    num_cores = len(schedule)
    makespan = 0
    _, ax = plt.subplots(figsize=(10, 6))
    for core, tasks in schedule.items():
        for task in tasks:
            makespan = max(makespan, task["duration"]+task["start_time"])
            ax.barh(core, task["duration"], left=task["start_time"], height=0.8, label=task["task"])

    ax.set_xlabel("Time")
    ax.set_ylabel("Processors")
    # ax.set_xticks(range(0, makespan, 250))
    ax.set_yticks(range(num_cores))
    ax.set_yticklabels([f"P{i}" for i in range(num_cores)])
    ax.set_title(f"Task Scheduling Visualization\nMakespan: {makespan}")
    plt.tight_layout()
    plt.savefig(f"figures/schedule_{makespan}.png")
    plt.show()

