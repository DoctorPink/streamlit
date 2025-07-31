import streamlit as st
import pandas as pd
import numpy as np

st.title('NYC Uber Pickups - Updated')
st.divider(width="stretch")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# https://github.github.com/gfm/ Markdown

@st.cache_data
# -----------------------------Create the data frame -----------------------------
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Data is cached for fast loading.")

# -----------------------------Show Raw Data Table -----------------------------
if st.checkbox('Show Data in a Table'):
  st.subheader('NYC Uber Pickups for One Day')
  st.write(data)

# -----------------------------Show  Bar Chart -----------------------------
if st.checkbox('Show Data in a Histogram'): 
  st.html('<h2 style="color:#FD5DA8">Number of Pickups By Hour</h2>')
  hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
  st.bar_chart(hist_values, color="#FD5DA8")
  st.html('<hr style="border-top: 4px solid #FD5DA8;">')
  
# -----------------------------Show  Map -----------------------------

on = st.toggle("Turn the Filter On or Off")

if on:
  # --------- Map all Data Data --------  
  with st.container(border=True): 
    st.html('<h2 style="color:#DA1884">Map Uber Pickups By Hour</h2>')
    hour_to_filter = st.slider('Select an hour to display:', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Filter Pickups at {hour_to_filter}:00')
    st.map(filtered_data, color="#FD5DA8")
else:
  # --------- Show  Map Filtered -------- 
  with st.container(border=True):
    st.html('<h2 style="color:#DA1884">Map of All Uber Pickups</h2>') 
    st.map(data, color="#FD5DA8")
  
