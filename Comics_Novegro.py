from pickle import TRUE
import streamlit as st
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
import numpy as np
from IPython.display import IFrame
import folium

locator = Nominatim(user_agent = "myapp")
location = locator.geocode("Via Novegro 20090 Segrate")
start_lat=location.latitude 
start_lng=location.longitude
nov_location={'lat': start_lat, 'lng': start_lng}
df = pd.DataFrame(data=nov_location, index=[1])
st.map(df)