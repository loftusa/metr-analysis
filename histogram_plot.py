"""Plot stacked histogram after flattening by removing from tallest bars."""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Buckets in order
buckets = [
    "1s", "2s", "3s", "4s", "8s", "16s", "32s",
    "1m", "2m", "4m", "8m", "16m", "32m",
    "1hr", "2hr", "4hr", "8hr",
]

# Source breakdown per bucket: {bucket: (SWAA, HCAST, RE-Bench)}
source_data = {
    "1s":  (6, 0, 0),
    "2s":  (6, 0, 0),
    "3s":  (20, 0, 0),
    "4s":  (21, 0, 0),
    "8s":  (7, 4, 0),
    "16s": (7, 0, 0),
    "32s": (1, 1, 0),
    "1m":  (0, 3, 0),
    "2m":  (0, 3, 0),
    "4m":  (0, 6, 0),
    "8m":  (0, 16, 0),
    "16m": (0, 14, 0),
    "32m": (0, 20, 0),
    "1hr": (0, 9, 0),
    "2hr": (0, 6, 0),
    "4hr": (0, 8, 2),
    "8hr": (0, 9, 5),
}

totals = {b: sum(source_data[b]) for b in buckets}
total_sum = sum(totals.values())
assert total_sum == 174, f"Expected 174, got {total_sum}"

# Remove 85 values by shaving from the tallest bars one at a time.
remaining = dict(totals)
to_remove = 85

for _ in range(to_remove):
    tallest = max(remaining, key=remaining.get)
    remaining[tallest] -= 1

removed_per_bucket = {b: totals[b] - remaining[b] for b in buckets}
assert sum(remaining.values()) == 174 - 85 == 89

print("After flattening:")
for b in buckets:
    print(f"  {b}: {totals[b]:2d} -> {remaining[b]:2d}  (removed {removed_per_bucket[b]})")

# Distribute remaining counts across sources proportionally.
final_sources = {}
for b in buckets:
    swaa, hcast, rebench = source_data[b]
    orig = totals[b]
    target = remaining[b]
    to_cut = orig - target

    sources = [swaa, hcast, rebench]
    for _ in range(to_cut):
        idx = max(range(3), key=lambda i: sources[i])
        sources[idx] -= 1

    final_sources[b] = tuple(sources)
    assert sum(sources) == target, f"{b}: expected {target}, got {sum(sources)}"

# Plot stacked bar chart
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 5.5))

x = np.arange(len(buckets))
width = 1.0

swaa_vals = [final_sources[b][0] for b in buckets]
hcast_vals = [final_sources[b][1] for b in buckets]
rebench_vals = [final_sources[b][2] for b in buckets]

# Colors matching the reference image — more saturated, less transparent
c_hcast = "#7B9FD4"
c_rebench = "#E8A87C"
c_swaa = "#82C882"

# Stack: HCAST on bottom, RE-Bench next, SWAA on top
ax.bar(x, hcast_vals, width, label="HCAST", color=c_hcast, alpha=0.55, edgecolor="none")
bottom_re = list(hcast_vals)
ax.bar(x, rebench_vals, width, bottom=bottom_re, label="RE-Bench", color=c_rebench, alpha=0.55, edgecolor="none")
bottom_swaa = [h + r for h, r in zip(hcast_vals, rebench_vals)]
ax.bar(x, swaa_vals, width, bottom=bottom_swaa, label="SWAA", color=c_swaa, alpha=0.55, edgecolor="none")

# X-axis: match the reference figure labels
x_labels = [
    "1 sec", "", "4 sec", "", "15 sec", "",
    "1 min", "", "4 min", "", "15 min", "", "1 hr", "", "4 hrs", "", "16 hrs",
]
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=10)

# Y-axis: match reference (0, 5, 10, 15, 20, 25)
ax.set_ylim(0, 25)
ax.set_yticks([0, 5, 10, 15, 20, 25])

ax.set_xlabel("Human task time", fontsize=12)
ax.set_ylabel("Number of tasks (stacked)", fontsize=12)
ax.set_title("Distribution of Task Difficulty", fontsize=14, fontweight="bold")
ax.legend(title="Task Source", loc="upper right", framealpha=0.9)

sns.despine(ax=ax)
plt.tight_layout()

out_path = "/Users/alex/Library/CloudStorage/Dropbox/Code/experiments/histogram_plot.png"
plt.savefig(out_path, dpi=150)
print(f"\nSaved to {out_path}")
