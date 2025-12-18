import os
import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Smart Blinds Dashboard", layout="wide")

st.title("☀️ Smart Blinds IoT Monitoring System")
st.markdown(
    "This dashboard monitors light intensity and controls blinds to optimize energy efficiency."
)

# =========================
# تحميل البيانات (مسار آمن)
# =========================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'iot final.xlsx')
    df = pd.read_excel(data_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

df = load_data()

# =========================
# Sidebar filters
# =========================
st.sidebar.header("Filter Data")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Timestamp'].min().date(), df['Timestamp'].max().date()]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[
        (df['Timestamp'].dt.date >= start_date) &
        (df['Timestamp'].dt.date <= end_date)
    ]

# =========================
# KPI Metrics
# =========================
col1, col2, col3 = st.columns(3)
latest_data = df.iloc[-1]

with col1:
    st.metric(
        label="🌡️ Current Temperature",
        value=f"{latest_data['Temp (°C)']} °C"
    )

with col2:
    st.metric(
        label="💡 Light Intensity",
        value=f"{latest_data['Light (Lux)']} Lux"
    )

with col3:
    status_color = "green" if latest_data['Blind Status'] == "Open" else "red"
    st.markdown(
        f"### 🪟 Blind Status: :{status_color}[{latest_data['Blind Status']}]"
    )

# =========================
# Time Series Plot
# =========================
st.subheader("📈 Light Intensity & Temperature Over Time")

fig = px.line(
    df,
    x='Timestamp',
    y=['Light (Lux)', 'Temp (°C)'],
    title="Sensors Telemetry",
    template="plotly_dark"
)

st.plotly_chart(fig, width='stretch')

# =========================
# Raw Data
# =========================
if st.checkbox("Show Raw Data"):
    st.dataframe(df)
