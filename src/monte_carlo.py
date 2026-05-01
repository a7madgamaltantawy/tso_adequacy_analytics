import numpy as np
import pandas as pd

def simulate_forced_outages(df: pd.DataFrame, forced_outage_rate: float, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = df.copy()
    outage_flag = rng.random(len(df)) < forced_outage_rate
    outage_size = rng.uniform(0.15, 0.45, len(df))
    df['thermal_available_mw'] = df['thermal_nominal_mw'] * (1 - outage_flag * outage_size)
    return df
