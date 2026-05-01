import pandas as pd
from data_loader import load_raw_timeseries, load_system_config, PROCESSED_DIR
from preprocessing import build_generation_timeseries
from monte_carlo import simulate_forced_outages
from adequacy_metrics import calculate_balance, calculate_kpis

def run_scenario(seed: int = 42) -> tuple[pd.DataFrame, dict]:
    config = load_system_config()
    df = load_raw_timeseries()
    df = build_generation_timeseries(df, config)
    df = simulate_forced_outages(df, float(config['forced_outage_rate']), seed=seed)
    df = calculate_balance(df)
    return df, calculate_kpis(df)

if __name__ == '__main__':
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df, kpis = run_scenario()
    df.to_csv(PROCESSED_DIR / 'adequacy_results.csv', index=False)
    pd.DataFrame([kpis]).to_csv(PROCESSED_DIR / 'adequacy_kpis.csv', index=False)
    print('Scenario completed')
    print(kpis)
