import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# Function to find the latest CSV file
def get_latest_csv():
    csv_files = [f for f in os.listdir('data') if f.lower().endswith('.csv') and 'visit' in f.lower()]
    if not csv_files:
        return None
    return max(csv_files, key=lambda x: os.path.getctime(os.path.join('data', x)))

# Read the CSV file
latest_csv = get_latest_csv()
if latest_csv:
    visit_df = pd.read_csv(f'data/{latest_csv}')
else:
    st.error("No suitable CSV file found.")
    st.stop()

# Create tdf
tdf = visit_df[["Office Location", "Visited By Email ID", "Created By", "Manager Job Title", "Manager", "Manager Email"]]

# Create CONCAT column
tdf['CONCAT'] = tdf['Office Location'] + tdf['Visited By Email ID'] + tdf['Created By'] + tdf['Manager Job Title']

# Keep only unique rows based on CONCAT
tdf = tdf.drop_duplicates(subset=['CONCAT'])

# Create Org_df
Org_df = tdf.copy()

# Filter Visit_df for dates after July 18, 2024
visit_df['Visit DateTime GMT'] = pd.to_datetime(visit_df['Visit DateTime GMT'])
visit_df = visit_df[visit_df['Visit DateTime GMT'] > datetime(2024, 7, 18)]

# Create Streamlit app
st.title('Visit Location Map')

# Create dropdowns
visited_by = st.selectbox('Visited by', ['All'] + list(Org_df['Created By'].unique()))
manager_job_title = st.selectbox('Manager Job Title', ['All'] + list(Org_df['Manager Job Title'].unique()))
office_location = st.selectbox('Office Location', ['All'] + list(Org_df['Office Location'].unique()))

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
