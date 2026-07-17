# Experiment Notes: Refactoring and Structural Changes

This document outlines the architectural changes, code refactoring decisions, and rationale for structural modifications implemented in this project.

## 1. Directory Structure Organization
To elevate the codebase to a production-ready, professional standard, we restructured the workspace as follows:
- **`data/`**: Created to house raw inputs (`historical_data.csv` and `fear_greed_index.csv`). This isolates massive raw data from source code and outputs.
- **`assets/`**: Created to house output visual assets (`sentiment_vs_pnl.png` and `sentiment_vs_size.png`). This prevents root-level clutter and organizes visual reports.

## 2. Refactoring notebook to `main.py`
We extracted and compiled the loose cells of `Assignment.ipynb` into a production-ready `main.py` script. The following key enhancements were made:
- **Pathing Standardization**: All file lookups and saves now use `os.path.join` to ensure cross-platform compatibility (Windows vs Unix-like OS).
- **Modularity**: Code was organized into functional blocks:
  - `load_data()`: Safely handles raw data loading with informative exception messaging.
  - `run_sentiment_analysis_pipeline()`: Cleanly merges date-standardized datasets, runs aggregations, and returns a JSON summary.
  - `generate_plots()`: Handles visualization logic.
- **Deprecation Fixes**: 
  - Fixed `FutureWarning: The ci parameter is deprecated. Use errorbar=None for the same effect.` by replacing `ci=None` with `errorbar=None`.
  - Fixed `FutureWarning: Passing palette without assigning hue is deprecated...` by explicitly passing `hue='classification'` and disabling the legend (`legend=False`) since classification is already on the x-axis.

## 3. Strict JSON Serialization
The JSON generator is configured to produce structured trader performance summaries grouped by market regime. The output (`pipeline_evaluation_output.json`) contains:
- **Metadata**: Execution timestamp, total records analyzed, status.
- **Metrics by Regime**: Total trades, win rate, average realized PnL (USD), and average position size (USD) for each sentiment classification (e.g. Extreme Fear, Extreme Greed, Fear, Greed, Neutral).
