import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load data
url = "Your_GitHub_CSV_URL_Here"
Visit_df = pd.read_csv(url)

# Streamlit app
st.title("Visit Map")

# Create selectbox
selected_creator = st.selectbox("Visited by", Visit_df["Created By"].unique())

# Filter dataframe
tdf = Visit_df[Visit_df["Created By"] == selected_creator]

# Create map
m = folium.Map()

# Add markers
for idx, row in tdf.iterrows():
    folium.Marker(
        [row["Visit Latitude"], row["Visit Longitude"]],
        popup=row["Created By"],
        icon=folium.Icon(color="green")
    ).add_to(m)

# Display map
folium_static(m)
