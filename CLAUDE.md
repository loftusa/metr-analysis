# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Analysis of METR agent benchmark data — exploring relationships between agent action counts, task difficulty (human_minutes), and task scores across multiple agent architectures and task families.

## Key Data

- **Action Counts.yaml** (~1.7MB): Raw benchmark data. Nested structure: `task_family > variant > run_id > {action_count, agent, human_minutes, score}`. 11,639 runs across 186 tasks, 106 agents.
- **viz_data.json**: Pre-processed aggregated metrics for the HTML dashboard.
- **action_counts_analysis.ipynb**: Main analysis notebook (polars-based; loads YAML, produces all plots in `plots/`).

## Commands

```bash
# Run standalone scripts
uv run histogram_plot.py

# Run notebook (execute in place)
uv run --with pyyaml --with polars --with pandas --with numpy --with matplotlib --with seaborn --with scikit-learn --with scipy --with jupyter --with ipykernel jupyter nbconvert --to notebook --execute action_counts_analysis.ipynb --output action_counts_analysis.ipynb
```

Dependencies are not listed in pyproject.toml — they are passed inline via `uv run --with`. Python 3.12. The notebook uses **polars** as the primary DataFrame library; pandas is imported only minimally for seaborn heatmap compatibility.

## Architecture

This is a notebook-driven analysis project, not a library or service. The primary artifact is `action_counts_analysis.ipynb`, which contains all data loading, analysis, and visualization code. `histogram_plot.py` is a separate standalone script for a specific stacked histogram visualization (task difficulty distribution by source: SWAA, HCAST, RE-Bench).

Generated plots go to `plots/`. The HTML dashboard (`agent_runs_dashboard.html`) reads from `viz_data.json`.

## Key Findings (from analysis)

- Action count vs score correlation (rho = −0.33) is **almost entirely confounded** by task difficulty. Within-task: median delta = −0.5 actions. Within (task, model): median delta = −0.8. The effect is real but tiny.
- Better models (claude-4-opus, claude-4-sonnet) are both more successful AND more action-efficient than older/weaker models.
- Models differ in failure behavior: Claude models persist (long failure tails), o1-preview gives up fast (1-5 actions for both success and failure).
- Insight-based tasks (reverse_hash, pico_ctf) show bimodal action counts: solve in 3-4 actions or grind 60-80+ uselessly.
- 18.6% of runs are safety evaluation variants (sabotage, refuse, tutor, unethical) — must be separated from capability analysis.
- Scoring is heterogeneous: 90 tasks binary, 68 tasks continuous/partial.
