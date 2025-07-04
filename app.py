import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ---------------------- Title ----------------------
st.set_page_config(page_title="Airline Demand Dashboard", layout="wide")
st.title("✈️ Airline Market Demand Dashboard (Live Data)")

# ---------------------- Data Fetch ----------------------
@st.cache_data(ttl=600)
def fetch_flight_data():
    try:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch data from API.")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# ---------------------- Data Processing ----------------------
def process_data(raw_data):
    try:
        columns = [
            'icao24', 'callsign', 'origin_country', 'time_position',
            'last_contact', 'longitude', 'latitude', 'baro_altitude',
            'on_ground', 'velocity', 'true_track', 'vertical_rate',
            'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source'
        ]
        df = pd.DataFrame(raw_data['states'], columns=columns)
        df = df.dropna(subset=['origin_country', 'latitude', 'longitude'])
        return df
    except Exception as e:
        st.error("Error processing data")
        return pd.DataFrame()

# ---------------------- Main Logic ----------------------
with st.spinner("Fetching live flight data..."):
    data = fetch_flight_data()

if data:
    df = process_data(data)

    # ---------------------- Filter UI ----------------------
    st.sidebar.header("🔍 Filter Options")
    countries = df['origin_country'].unique().tolist()
    selected_country = st.sidebar.selectbox("Filter by Origin Country", ["All"] + countries)

    if selected_country != "All":
        df = df[df['origin_country'] == selected_country]

    # ---------------------- Display Raw Data ----------------------
    with st.expander("📋 View Raw Data"):
        st.dataframe(df)

    # ---------------------- Insights ----------------------
    st.subheader("🌍 Top 10 Countries by Active Flights")
    country_count = df['origin_country'].value_counts().reset_index()
    country_count.columns = ['Country', 'Flights']
    fig1 = px.bar(country_count.head(10), x='Country', y='Flights', text='Flights',
                  title='Top 10 Origin Countries (Live Flights)',
                  labels={'Flights': 'No. of Active Flights'})
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------------- Flight Distribution Map ----------------------
    st.subheader("📌 Flight Positions on World Map")
    fig2 = px.scatter_geo(df,
                          lat='latitude',
                          lon='longitude',
                          color='origin_country',
                          hover_name='callsign',
                          title='Live Flight Positions',
                          opacity=0.7)
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No data available to display.")

# ---------------------- Footer ----------------------
st.markdown("""
---
✅ Developed as part of a technical assessment task.  
📊 Data Source: [OpenSky Network](https://opensky-network.org/)  
""")
