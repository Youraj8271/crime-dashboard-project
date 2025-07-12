import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(layout="wide", page_title="Crime Dashboard")
st.title("🛡️ Real-Time Crime Rate Dashboard – India")

# Load data
df = pd.read_csv("crime_data_fixed.csv", parse_dates=['Date'])

# Rename columns for map compatibility
df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)

# Show map (all data)
st.subheader("🗺️ Crime Map (All Data)")
st.map(df[['latitude', 'longitude']])

# Sidebar filters
st.sidebar.header("📊 Filters")
states = st.sidebar.multiselect("Select State", df["State"].unique())
cities = st.sidebar.multiselect("Select City", df["City"].unique())
crime_types = st.sidebar.multiselect("Crime Type", df["Crime_Type"].unique())
status_filter = st.sidebar.selectbox("Status", ["All", "Solved", "Pending"])

# Apply filters
if states:
    df = df[df["State"].isin(states)]

if crime_types:
    df = df[df["Crime_Type"].isin(crime_types)]
if status_filter != "All":
    df = df[df["Status"] == status_filter]

# KPIs
st.subheader("📊 Key Statistics")
col1, col2 = st.columns(2)
col1.metric("🔢 Total Crimes", len(df))
top_crime = df["Crime_Type"].mode()[0] if not df.empty else "-"
col2.metric("🚨 Top Crime Type", top_crime)

# Charts
col3, col4 = st.columns(2)
with col3:
    fig = px.histogram(df, x="Crime_Type", color="Status", title="Crime Type Distribution")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    if not df.empty:
        fig2 = px.line(df.sort_values("Date"), x="Date", title="Crime Trend Over Time")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data available for the selected filters to display line chart.")

# Filtered Map
st.subheader("📍 Filtered Crime Map")
if not df.empty:
    st.map(df[['latitude', 'longitude']])
else:
    st.warning("No map data for the selected filters.")

# Data Table
st.subheader("📋 Data Table")
st.dataframe(df)

# Footer
# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 18px; padding-top: 10px;'>
        🖋️ Developed by <b>Youraj Kumar</b><br>
        🎓 <span style='color: #1f77b4; font-weight: bold;'>  – IIT Patna</span>
    </div>
    """,
    unsafe_allow_html=True
)
