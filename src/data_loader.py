from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'

def load_raw_timeseries() -> pd.DataFrame:
    files = {
        'load_mw': RAW_DIR / 'load_profile.csv',
        'solar_cf': RAW_DIR / 'solar_capacity_factor.csv',
        'wind_cf': RAW_DIR / 'wind_capacity_factor.csv',
    }
    dfs = []
    for value_name, path in files.items():
        df = pd.read_csv(path, parse_dates=['timestamp'])
        dfs.append(df.rename(columns={'value': value_name}))
    out = dfs[0]
    for df in dfs[1:]:
        out = out.merge(df, on='timestamp', how='inner')
    return out

def load_system_config() -> dict:
    config = pd.read_csv(RAW_DIR / 'system_config.csv')
    return dict(zip(config['parameter'], config['value']))
