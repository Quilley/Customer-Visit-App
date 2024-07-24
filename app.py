import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# Function to find the latest CSV file
def get_latest_csv(directory='data'):
    csv_files = [f for f in os.listdir(directory) if f.lower().endswith('.csv') and 'visit' in f.lower()]
    if not csv_files:
        return None
    return os.path.join(directory, max(csv_files, key=lambda x: os.path.getctime(os.path.join(directory, x))))

# Read the CSV file
@st.cache_data
def load_data():
    csv_path = get_latest_csv()
    if csv_path:
        df = pd.read_csv(csv_path)
        df['Visit DateTime GMT'] = pd.to_datetime(df['Visit DateTime GMT'])
        return df
    return None

# Main function to run the Streamlit app
def main():
    st.title('Visit Location Map')

    # Load data
    visit_df = load_data()

    if visit_df is None:
        st.error("No suitable CSV file found.")
        return

    # Filter visits after July 18, 2024
    visit_df = visit_df[visit_df['Visit DateTime GMT'] > datetime(2024, 7, 18)]

    # Create dropdowns
    visited_by = st.selectbox('Visited by', ['All'] + list(visit_df['Created By'].unique()))
    manager_job_title = st.selectbox('Manager Job Title', ['All'] + list(visit_df['Manager Job Title'].unique()))
    office_location = st.selectbox('Office Location', ['All'] + list(visit_df['Office Location'].unique()))

    # Filter data based on selections
    filtered_df = visit_df.copy()
    if visited_by != 'All':
        filtered_df = filtered_df[filtered_df['Created By'] == visited_by]
    if manager_job_title != 'All':
        filtered_df = filtered_df[filtered_df['Manager Job Title'] == manager_job_title]
    if office_location != 'All':
        filtered_df = filtered_df[filtered_df['Office Location'] == office_location]

    # Create map
    m = folium.Map()

    # Add markers
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['Visit Latitude'], row['Visit Longitude']],
            popup=row['Created By']
        ).add_to(m)

    # Fit map to markers
    if not filtered_df.empty:
        sw = filtered_df[['Visit Latitude', 'Visit Longitude']].min().values.tolist()
        ne = filtered_df[['Visit Latitude', 'Visit Longitude']].max().values.tolist()
        m.fit_bounds([sw, ne])

    # Display map
    folium_static(m)

if __name__ == "__main__":
    main()
