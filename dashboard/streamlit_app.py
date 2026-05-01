from pathlib import Path
import sys
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'src'))

from scenarios import run_scenario

st.set_page_config(page_title='TSO Adequacy Analytics', layout='wide')
st.title('TSO Adequacy Analytics')
st.caption('PECD-style renewable profiles, Monte Carlo outages, and adequacy KPIs')

seed = st.sidebar.number_input('Monte Carlo seed', min_value=1, max_value=9999, value=42)
df, kpis = run_scenario(seed=int(seed))

c1, c2, c3, c4 = st.columns(4)
c1.metric('LOLE hours', kpis['LOLE_hours'])
c2.metric('EENS MWh', kpis['EENS_MWh'])
c3.metric('Peak load MW', kpis['Peak_Load_MW'])
c4.metric('Min reserve margin MW', kpis['Minimum_Reserve_Margin_MW'])

st.subheader('Hourly supply-demand balance')
plot_df = df[['timestamp', 'load_mw', 'available_generation_mw', 'reserve_margin_mw']].melt('timestamp')
st.plotly_chart(px.line(plot_df, x='timestamp', y='value', color='variable'), use_container_width=True)

st.subheader('Renewable capacity factors')
cf_df = df[['timestamp', 'solar_cf', 'wind_cf']].melt('timestamp')
st.plotly_chart(px.line(cf_df, x='timestamp', y='value', color='variable'), use_container_width=True)

st.subheader('Shortage hours')
st.dataframe(df[df['shortage_mw'] > 0][['timestamp', 'load_mw', 'available_generation_mw', 'shortage_mw']], use_container_width=True)
