import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Function to load data from GitHub
@st.cache_data
def load_data_from_github():
    # GitHub raw file URL
    url = 'https://github.com/Quilley/Customer-Visit-App/blob/main/Visit%20Logs%20(6).csv'
    
    # Read CSV file from URL
    visit_df = pd.read_csv(url)

    # Create a new temporary dataframe
    tdf = visit_df[['Office Location', 'Visited By Email ID', 'Created By', 'Manager Job Title', 'Manager', 'Manager Email']].copy()

    # Create a "CONCAT" column
    tdf['CONCAT'] = (tdf['Office Location'] + tdf['Visited By Email ID'] + tdf['Created By'] +
                     tdf['Manager Job Title'] + tdf['Manager'] + tdf['Manager Email'])

    # Remove duplicates based on the "CONCAT" column
    tdf = tdf.drop_duplicates(subset=['CONCAT'])

    # Move tdf to Org_df
    Org_df = tdf.copy()

    # Filter visit_df based on the date
    visit_df['Visit DateTime GMT'] = pd.to_datetime(visit_df['Visit DateTime GMT'])
    visit_df = visit_df[visit_df['Visit DateTime GMT'] > datetime(2024, 7, 18)]

    return visit_df, Org_df

# Load the data
visit_df, Org_df = load_data_from_github()

# Streamlit UI
st.title("Visit Logs Analysis")

# Dropdown for "Visited by"
visited_by_options = Org_df['Created By'].unique()
selected_visited_by = st.selectbox("Visited by", visited_by_options, index=0)

# Function to create the Folium map
def create_map(data, selected_visited_by):
    # Initialize the map
    m = folium.Map(location=[data['Visit Latitude'].mean(), data['Visit Longitude'].mean()], zoom_start=2)

    # Filter data based on selected "Created By"
    if selected_visited_by:
        data = data[data['Created By'] == selected_visited_by]

    # Add markers to the map
    for idx, row in data.iterrows():
        folium.Marker(
            location=[row['Visit Latitude'], row['Visit Longitude']],
            popup=row['Created By']
        ).add_to(m)

    return m

# Create the map
folium_map = create_map(visit_df, selected_visited_by)

# Display the map in Streamlit
st_folium(folium_map, width=800, height=600)
