import pandas as pd

def build_generation_timeseries(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    df = df.copy()
    df['solar_mw'] = df['solar_cf'] * float(config['solar_capacity_mw'])
    df['wind_mw'] = df['wind_cf'] * float(config['wind_capacity_mw'])
    df['thermal_nominal_mw'] = float(config['thermal_capacity_mw'])
    df['import_capacity_mw'] = float(config['import_capacity_mw'])
    return df
