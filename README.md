# ✈️ Airline Market Demand Dashboard

A Streamlit web app that fetches live flight data from the [OpenSky Network](https://opensky-network.org/), displays real-time trends, and visualizes active flights on a world map.

## 🚀 Features

- Live data fetching using OpenSky API
- Interactive bar chart of most active origin countries
- Flight distribution on world map (Geo scatter)
- Sidebar filter to view data by origin country
- Auto-refreshing with cache for performance

## 📦 Tech Stack

- Python
- Streamlit
- Pandas
- Requests
- Plotly

## 🛠️ How to Run the App Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/airline-demand-app.git
cd airline-demand-app

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
