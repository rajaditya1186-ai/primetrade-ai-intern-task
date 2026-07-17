import os
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """
    Loads raw blockchain trading data and market sentiment index from the data directory.
    """
    fg_path = os.path.join('data', 'fear_greed_index.csv')
    hist_path = os.path.join('data', 'historical_data.csv')
    
    if not os.path.exists(fg_path) or not os.path.exists(hist_path):
        raise FileNotFoundError(
            f"Required CSV files not found in 'data/' directory. "
            f"Expected: {fg_path} and {hist_path}"
        )
    
    fg_df = pd.read_csv(fg_path)
    hist_df = pd.read_csv(hist_path)
    print("Files successfully loaded from 'data/' directory.")
    return fg_df, hist_df

def run_sentiment_analysis_pipeline(fg_df, hist_df):
    """
    Cleans raw blockchain trading data, pairs it with market sentiment index,
    and returns a structured JSON summary evaluating trader performance.
    """
    # 1. Standardize and parse dates (Data Engineering)
    fg_df['date_clean'] = pd.to_datetime(fg_df['date']).dt.date
    hist_df['date_clean'] = pd.to_datetime(hist_df['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce').dt.date

    # Drop records with malformed dates
    hist_df.dropna(subset=['date_clean'], inplace=True)

    # 2. Merge datasets
    merged_df = pd.merge(hist_df, fg_df[['date_clean', 'value', 'classification']], on='date_clean', how='inner')

    # Helper classifications
    merged_df['is_win'] = merged_df['Closed PnL'] > 0
    merged_df['is_loss'] = merged_df['Closed PnL'] < 0

    # 3. Aggregate Performance Analytics
    sentiment_groups = merged_df.groupby('classification')

    metrics_output = {
        "metadata": {
            "pipeline_run_timestamp": datetime.now().isoformat(),
            "total_records_analyzed": len(merged_df),
            "status": "SUCCESS"
        },
        "metrics_by_regime": {}
    }

    for name, group in sentiment_groups:
        total = int(group['Closed PnL'].count())
        wins = int(group['is_win'].sum())
        losses = int(group['is_loss'].sum())

        metrics_output["metrics_by_regime"][name] = {
            "total_trades": total,
            "win_rate": round(wins / (wins + losses), 4) if (wins + losses) > 0 else 0.0,
            "avg_pnl_usd": round(float(group['Closed PnL'].mean()), 2),
            "avg_position_size_usd": round(float(group['Size USD'].mean()), 2)
        }

    # 4. Enforce strict JSON output serialization
    strict_json_output = json.dumps(metrics_output, indent=4)
    return strict_json_output, merged_df

def generate_plots(merged_df):
    """
    Generates and saves visual analysis reports (visualizing regime vs PnL/size) to 'assets/' folder.
    """
    os.makedirs('assets', exist_ok=True)
    
    # Set plot aesthetics
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Average realized performance per emotional phase
    plt.figure(figsize=(10, 5))
    sns.barplot(data=merged_df, x='classification', y='Closed PnL', errorbar=None, palette='coolwarm', hue='classification', legend=False)
    plt.title('Average Realized PnL per Trade across Market Regimes')
    plt.xlabel('Market Regime (Fear & Greed Index)')
    plt.ylabel('Avg realized PnL ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    pnl_plot_path = os.path.join('assets', 'sentiment_vs_pnl.png')
    plt.savefig(pnl_plot_path, dpi=300)
    plt.close()
    print(f"Chart 1 saved to: {pnl_plot_path}")

    # Chart 2: Capital risk concentration
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=merged_df, x='classification', y='Size USD', showfliers=False, palette='viridis', hue='classification', legend=False)
    plt.title('Capital Size Distribution vs Market Regimes')
    plt.xlabel('Market Regime (Fear & Greed Index)')
    plt.ylabel('Position Size ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    size_plot_path = os.path.join('assets', 'sentiment_vs_size.png')
    plt.savefig(size_plot_path, dpi=300)
    plt.close()
    print(f"Chart 2 saved to: {size_plot_path}")

def main():
    print("Starting pipeline execution...")
    
    # 1. Load Data
    fg_df, hist_df = load_data()
    
    # 2. Run pipeline
    json_result, merged_df = run_sentiment_analysis_pipeline(fg_df, hist_df)
    
    # 3. Save JSON evaluation output
    output_path = 'pipeline_evaluation_output.json'
    with open(output_path, 'w') as f:
        f.write(json_result)
    print(f"Strict JSON output saved to: {output_path}")
    print(json_result)
    
    # 4. Generate & save plots
    generate_plots(merged_df)
    print("Pipeline execution completed successfully.")

if __name__ == '__main__':
    main()
