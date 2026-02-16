# METR Agent Action Counts Analysis

Analysis of 11,639 agent runs across 186 tasks and 106 agents from the METR benchmark, exploring the relationship between action counts, task difficulty, and agent success.

## Key Findings

**The headline "more actions = worse" correlation (rho = −0.33) is almost entirely a confound.** Task difficulty drives both action count (+0.47) and score (−0.40). Within the same task, successful and failed runs use nearly the same number of actions (median delta = −0.5). Even controlling for both task and model, the effect is tiny (median delta = −0.8).

**Better models are more successful AND more action-efficient.** Claude-4-opus achieves 80% success with median 9 actions; gpt-4o-mini manages 49% with median 11. Stronger models maintain high success rates for more actions before the declining curve kicks in.

**Models differ in how they fail.** Claude models persist when stuck (failure tails extending to 50+ actions). O1-preview gives up fast (both successes and failures concentrated at 1-5 actions). This is partly a scaffolding effect — the dragonfly framework lets gpt-4o grind to 484 actions, while duet caps the same model around 50.

**Insight-based tasks produce bimodal action counts.** Tasks like `reverse_hash` and `pico_ctf` are either solved in 3-4 actions or ground on for 60-80+ uselessly. More actions genuinely don't help on these.

**18.6% of runs are safety evaluations** (sabotage, refuse, tutor, unethical variants) mixed in with capability runs — these must be separated for capability analysis.

## Plots

All plots are in `plots/`. Key visualizations:

| Plot | Description |
|------|-------------|
| `01_score_distribution` | Bimodal: 40% zeros, 45% ones, 15% partial |
| `02_action_count_by_outcome` | Successes concentrated at low action counts; failures spread wide |
| `03_confound_check` | Difficulty correlates with both action count and score |
| `04_within_task_delta` | Within-task, success/failure action counts are nearly equal |
| `05_action_limits` | Smooth distribution — no round-number censoring spikes |
| `06_model_comparison` | Model efficiency frontier: score vs actions |
| `07_per_model_action_outcome` | Per-model success/failure action distributions |
| `08_success_vs_actions_per_model` | Declining success curves, model-shifted |
| `09_within_task_model_delta` | Cleanest test: within (task, model) pairs |
| `10_task_families` | Task family landscape: success rate vs mean actions |
| `11_grinding_agents` | Which agents grind when failing (dragonfly is the outlier) |

## Data

- **Action Counts.yaml** (~1.7MB): Raw benchmark data. Nested YAML: `task_family > variant > run_id > {action_count, agent, human_minutes, score}`.
- **viz_data.json**: Pre-processed metrics for the HTML dashboard.

## Running

```bash
# Execute the notebook
uv run --with pyyaml --with polars --with pandas --with numpy --with matplotlib \
       --with seaborn --with scikit-learn --with scipy --with jupyter --with ipykernel \
       jupyter nbconvert --to notebook --execute action_counts_analysis.ipynb \
       --output action_counts_analysis.ipynb

# Standalone histogram script
uv run histogram_plot.py
```

Python 3.12. Dependencies are passed inline via `uv run --with` (not in pyproject.toml). The notebook uses **polars** as the primary DataFrame library.
