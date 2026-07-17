# Market Sentiment vs. Trader Performance Analysis

This project cleans raw blockchain trading data, pairs it with the Crypto Fear & Greed Index (market sentiment index), and evaluates trader performance across different market emotional regimes.

## Project Structure

```text
├── data/
│   ├── historical_data.csv        # Raw blockchain trading transactions
│   └── fear_greed_index.csv       # Daily market sentiment classifications
├── assets/
│   ├── sentiment_vs_pnl.png       # Chart: Average Realized PnL vs. Market Regime
│   └── sentiment_vs_size.png      # Chart: Position Size Distribution vs. Market Regime
├── main.py                        # Executable data engineering and analysis pipeline
├── pipeline_evaluation_output.json # Structured JSON metrics report
├── experiment_notes.md            # Structural refactoring and code execution notes
└── README.md                      # Setup instructions, run steps, and core discoveries (this file)
```

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Dependency Installation
Install the required packages using `pip`:
```bash
pip install pandas matplotlib seaborn
```

## Running the Pipeline

To run the pipeline and regenerate the JSON summary and analytical charts:
```bash
python main.py
```

Upon execution, the script will:
1. Load datasets safely from the `data/` directory.
2. Align daily sentiment indexes with transaction timestamps.
3. Calculate metrics (win rate, average PnL, average size) grouped by regime.
4. Output `pipeline_evaluation_output.json` to the root folder.
5. Generate and save diagnostic plots inside the `assets/` directory.

---

## Core Discoveries & Insights

Analyzing the processed metrics of **211,218 trades** across different emotional phases yields several major discoveries:

### 1. Sentiment Regimes Performance Summary
| Market Regime | Total Trades | Win Rate | Avg. PnL (USD) | Avg. Position Size (USD) |
|---|---|---|---|---|
| **Extreme Fear** | 21,400 | 76.22% | $34.54 | $5,349.73 |
| **Fear** | 61,837 | 87.29% | $54.29 | $7,816.11 |
| **Neutral** | 37,686 | 82.39% | $34.31 | $4,782.73 |
| **Greed** | 50,303 | 76.89% | $42.74 | $5,736.88 |
| **Extreme Greed** | 39,992 | 89.17% | $67.89 | $3,112.25 |

### 2. Key Takeaways & Market Observations
- **Peak Profitability & Caution during Extreme Greed**: 
  Traders achieved their highest win rate (**89.17%**) and average realized PnL (**$67.89**) during *Extreme Greed*. However, their average position size was the lowest (**$3,112.25**), implying that while traders are highly successful in capitalizing on strong momentum, they aggressively de-risk and keep position sizes small to avoid sudden reversals.
  
- **Capital Aggression during Fear**:
  During *Fear*, traders deployed their largest position sizes by far (**$7,816.11** on average), resulting in a high win rate (**87.29%**) and a solid average realized PnL of **$54.29**. This suggests a high-conviction "buy-the-dip" behavior where traders seize opportunities in a fearful market with larger position size allocations.
  
- **Vulnerability in Extreme Fear**:
  *Extreme Fear* recorded the lowest win rate (**76.22%**) and a weak average realized PnL (**$34.54**), highlighting the difficulty of navigating extreme panic and volatility, even with moderate position sizes.
