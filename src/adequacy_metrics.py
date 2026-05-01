import pandas as pd

def calculate_balance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['available_generation_mw'] = (
        df['solar_mw'] + df['wind_mw'] + df['thermal_available_mw'] + df['import_capacity_mw']
    )
    df['shortage_mw'] = (df['load_mw'] - df['available_generation_mw']).clip(lower=0)
    df['surplus_mw'] = (df['available_generation_mw'] - df['load_mw']).clip(lower=0)
    df['reserve_margin_mw'] = df['available_generation_mw'] - df['load_mw']
    return df

def calculate_kpis(df: pd.DataFrame) -> dict:
    return {
        'LOLE_hours': int((df['shortage_mw'] > 0).sum()),
        'EENS_MWh': round(float(df['shortage_mw'].sum()), 2),
        'Peak_Load_MW': round(float(df['load_mw'].max()), 2),
        'Minimum_Reserve_Margin_MW': round(float(df['reserve_margin_mw'].min()), 2),
    }
